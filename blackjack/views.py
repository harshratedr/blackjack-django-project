from datetime import date
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import PlayerProfile, TransactionHistory
from .game_logic import get_deck, deal_card, hand_value
from .forms import RegisterForm, LoginForm  # type: ignore

@login_required
def game(request):
    player_profile, _ = PlayerProfile.objects.get_or_create(user=request.user)
    chip_pool = player_profile.credits

    
    if request.method == 'GET' and 'reset' in request.GET:  
        reset_game_session(request)
        return redirect('game')

   
    today = date.today()
    if player_profile.last_login_date != today:
        give_daily_bonus(player_profile)

    
    if 'deck' not in request.session:
        initialize_game_session(request)

   
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'bet':
            handle_bet(request, player_profile, chip_pool)
        elif action == 'hit':
            handle_hit(request, player_profile)
        elif action == 'stand':
            handle_stand(request, player_profile)
        elif action == 'double_down':
            handle_double_down(request, player_profile)

    
    context = {
        'player_hand': request.session.get('player_hand', []),
        'dealer_hand': request.session.get('dealer_hand', []),
        'player_score': request.session.get('player_score', 0),
        'dealer_score': request.session.get('dealer_score', 0),
        'balance': chip_pool,
        'bet': request.session.get('bet', 0),
        'game_over': request.session.get('game_over', False),
        'result': request.session.get('result', None),
    }
    return render(request, 'blackjack/game.html', context)


def handle_double_down(request, player_profile):

    bet_amount = request.session['bet']
    chip_pool = player_profile.credits

    if bet_amount * 2 > chip_pool:
        return render(request, 'blackjack/game.html', {'error': "You cannot double down more than you have!", 'balance': chip_pool})

    player_profile.credits -= bet_amount 
    request.session['bet'] = bet_amount * 2  
    player_profile.save()

    log_transaction(player_profile, 'Double Down', bet_amount) 
    handle_hit(request, player_profile)  

    if not request.session['game_over']: 
        handle_stand(request, player_profile)


def reset_game_session(request):
    
    keys_to_reset = ['deck', 'player_hand', 'dealer_hand', 'player_score', 'dealer_score', 'bet', 'game_over', 'result']
    for key in keys_to_reset:
        request.session.pop(key, None)



def give_daily_bonus(player_profile):
    
    player_profile.credits += 100
    player_profile.last_login_date = date.today()
    player_profile.save()
    TransactionHistory.objects.create(player=player_profile, transaction_type='Bonus', amount=100)



def initialize_game_session(request):
    
    request.session['deck'] = get_deck()
    random.shuffle(request.session['deck'])
    request.session['player_hand'] = []
    request.session['dealer_hand'] = []
    request.session['player_score'] = 0
    request.session['dealer_score'] = 0
    request.session['bet'] = 0
    request.session['game_over'] = False
    request.session['result'] = None



def handle_bet(request, player_profile, chip_pool):
    
    bet_amount = int(request.POST.get('bet_amount'))
    if bet_amount > chip_pool:
        return render(request, 'blackjack/game.html', {'error': "You cannot bet more than you have!", 'balance': chip_pool})

    
    request.session['bet'] = bet_amount
    player_profile.credits -= bet_amount
    player_profile.save()
    log_transaction(player_profile, 'Bet', bet_amount)

    
    if bet_amount > player_profile.highest_bet:
        player_profile.highest_bet = bet_amount
        player_profile.save()

   
    deal_initial_cards(request)



def deal_initial_cards(request):
    
    request.session['player_hand'] = [deal_card(request.session['deck']), deal_card(request.session['deck'])]
    request.session['dealer_hand'] = [deal_card(request.session['deck']), deal_card(request.session['deck'])]
    request.session['player_score'] = hand_value(request.session['player_hand'])
    request.session['dealer_score'] = hand_value(request.session['dealer_hand'])



def handle_hit(request, player_profile):
    
    request.session['player_hand'].append(deal_card(request.session['deck']))
    request.session['player_score'] = hand_value(request.session['player_hand'])
    if request.session['player_score'] > 21:
        end_game_with_loss(request, player_profile)



def end_game_with_loss(request, player_profile):
    
    request.session['game_over'] = True
    request.session['result'] = 'You bust! Dealer wins.'
    player_profile.credits -= request.session['bet']
    player_profile.total_losses += 1
    player_profile.save()
    log_transaction(player_profile, 'Loss', request.session['bet'])



def handle_stand(request, player_profile):
    
    while hand_value(request.session['dealer_hand']) < 17:
        request.session['dealer_hand'].append(deal_card(request.session['deck']))
    request.session['dealer_score'] = hand_value(request.session['dealer_hand'])
    request.session['game_over'] = True
    determine_winner(request, player_profile)




def determine_winner(request, player_profile):
    
    
    player_score = request.session['player_score']
    dealer_score = request.session['dealer_score']
    bet_amount = request.session['bet']

    if dealer_score > 21 or player_score > dealer_score:
        request.session['result'] = 'You win!'
        player_profile.credits += bet_amount * 2
        player_profile.total_wins += 1
        log_transaction(player_profile, 'Win', bet_amount * 2)
    elif player_score < dealer_score:
        request.session['result'] = 'Dealer wins!'
        player_profile.credits -= bet_amount
        player_profile.total_losses += 1
        log_transaction(player_profile, 'Loss', bet_amount)
    else:
        request.session['result'] = "It's a tie!"
        player_profile.credits += bet_amount

    player_profile.save()




def log_transaction(player_profile, transaction_type, amount):
    
    TransactionHistory.objects.create(player=player_profile, transaction_type=transaction_type, amount=amount)



@login_required
def user_stats(request):
    player_profile = PlayerProfile.objects.get(user=request.user)
    transaction_history = TransactionHistory.objects.filter(player=player_profile).order_by('-timestamp')
    context = {
        'player_profile': player_profile,
        'transaction_history': transaction_history,
    }
    return render(request, 'blackjack/user_stats.html', context)



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            PlayerProfile.objects.create(user=user)
            login(request, user)
            return redirect('game')
    else:
        form = RegisterForm()
    return render(request, 'blackjack/register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('game')
    else:
        form = LoginForm()
    return render(request, 'blackjack/login.html', {'form': form})




def user_logout(request):
    logout(request)
    return redirect('login')




@login_required
def user_profile(request):
    player_profile = PlayerProfile.objects.get(user=request.user)
    transaction_history = TransactionHistory.objects.filter(player=player_profile).order_by('-timestamp')
    context = {
        'player_profile': player_profile,
        'transaction_history': transaction_history,
    }
    return render(request, 'blackjack/user_profile.html', context)




@login_required
def leaderboard(request):
    top_players = PlayerProfile.objects.order_by('-credits')[:10]
    context = {
        'top_players': top_players,
    }
    return render(request, 'blackjack/leaderboard.html', context)


@login_required
def buy_chips(request):
    player_profile = PlayerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        if amount > 0:
            player_profile.credits += amount
            player_profile.save()
            log_transaction(player_profile, 'Buy Chips', amount)  
            return redirect('game')  

    return render(request, 'blackjack/buy_chips.html', {'balance': player_profile.credits})
