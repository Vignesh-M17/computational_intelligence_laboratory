CODE:
male(motilal_nehru).
male(jawaharlal_nehru).
male(feroze_gandhi).
male(rajiv_gandhi).
male(sanjay_gandhi).
male(rahul_gandhi).
male(varun_gandhi).
male(robert_vadra).
male(raihan_vadra).
female(swarup_rani_nehru).
female(kamala_nehru).
female(indira_gandhi).
female(sonia_gandhi).
female(maneka_gandhi).
female(priyanka_gandhi).
female(miraya_vadra).
female(vijaya_lakshmi_pandit).
female(krishna_hutheesing).
married(motilal_nehru, swarup_rani_nehru).
married(jawaharlal_nehru, kamala_nehru).
married(feroze_gandhi, indira_gandhi).
married(rajiv_gandhi, sonia_gandhi).
married(sanjay_gandhi, maneka_gandhi).
married(robert_vadra, priyanka_gandhi).
spouse(X, Y) :- married(X, Y).
spouse(X, Y) :- married(Y, X).
parent(motilal_nehru, jawaharlal_nehru).
parent(swarup_rani_nehru, jawaharlal_nehru).
parent(motilal_nehru, vijaya_lakshmi_pandit).
parent(swarup_rani_nehru, vijaya_lakshmi_pandit).
parent(motilal_nehru, krishna_hutheesing).
parent(swarup_rani_nehru, krishna_hutheesing).
parent(jawaharlal_nehru, indira_gandhi).
parent(kamala_nehru, indira_gandhi).
parent(indira_gandhi, rajiv_gandhi).
parent(feroze_gandhi, rajiv_gandhi).
parent(indira_gandhi, sanjay_gandhi).
parent(feroze_gandhi, sanjay_gandhi).
parent(rajiv_gandhi, rahul_gandhi).
parent(sonia_gandhi, rahul_gandhi).
parent(rajiv_gandhi, priyanka_gandhi).
parent(sonia_gandhi, priyanka_gandhi).
parent(sanjay_gandhi, varun_gandhi).
parent(maneka_gandhi, varun_gandhi).
parent(priyanka_gandhi, raihan_vadra).
parent(robert_vadra, raihan_vadra).
parent(priyanka_gandhi, miraya_vadra).
parent(robert_vadra, miraya_vadra).
father(F, C) :- parent(F, C), male(F).
mother(M, C) :- parent(M, C), female(M).
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.
brother(B, X) :- sibling(B, X), male(B).
sister(S, X) :- sibling(S, X), female(S).
uncle(U, C) :-
    parent(P, C),
    brother(U, P).
aunt(A, C) :-
    parent(P, C),
    sister(A, P).
grandparent(GP, C) :-
    parent(GP, P),
    parent(P, C).
grandfather(GF, C) :- grandparent(GF, C), male(GF).
grandmother(GM, C) :- grandparent(GM, C), female(GM).

OUTPUT:
?- father(F, rahul_gandhi).
F = rajiv_gandhi .

?- sibling(S, rajiv_gandhi).
S = sanjay_gandhi .

?- uncle(U,raihan_vadra).
U = rahul_gandhi .

?- spouse(motilal_nehru, swarup_rani_nehru).
true .

?- grandparent(GP, priyanka_gandhi).
GP = indira_gandhi ;
GP = feroze_gandhi .

?- uncle(sanjay_gandhi,raihan_vadra).
false.

?- aunt(A,raihan_vadra).
false.
[23bcs123@mepcolinux ex6]$cat p2.pl
CODE:
:- use_module(library(apply)).
:- initialization(main).
main :-
    write('Enter operation (+, -, *, /, mod, **, square): '),
    read(Op),
    (
        Op == square ->
            write('Enter a number: '),
            read(X),
            R is X * X,
            write('Result: '), write(R), nl
    ;
        write('How many numbers? '),
        read(N),
        read_numbers(N, List),
        calculate(Op, List, R),
        write('Result: '), write(R), nl
    ).
read_numbers(0, []).
read_numbers(N, [X|T]) :-
    N > 0,
    write('Enter number: '),
    read(X),
    N1 is N - 1,
    read_numbers(N1, T).
calculate(+,   [H|T], R) :- foldl(add, T, H, R).
calculate(-,   [H|T], R) :- foldl(sub, T, H, R).
calculate(*,   [H|T], R) :- foldl(mul, T, H, R).
calculate(/,   [H|T], R) :- foldl(div, T, H, R).
calculate(mod, [H|T], R) :- foldl(mod_op, T, H, R).
calculate(**,  [H|T], R) :- foldl(pow, T, H, R).
add(X,A,B) :- B is A + X.
sub(X,A,B) :- B is A - X.
mul(X,A,B) :- B is A * X.
div(X,A,B) :- B is A / X.
mod_op(X,A,B) :- B is A mod X.
pow(X,A,B) :- B is A ** X.

OUTPUT:
?- main.
Enter operation (+, -, *, /, mod, **, square): *
|: .
How many numbers? |: 3.
Enter number: |: 1.
Enter number: |: 2.
Enter number: |: 3.
Result: 6
true .

?- main.
Enter operation (+, -, *, /, mod, **, square): square
|: .
Enter a number: |: 2.
Result: 4
true.

?- main.
Enter operation (+, -, *, /, mod, **, square): /
|: .
How many numbers? |: 2.
Enter number: |: 15.
Enter number: |: 3.
Result: 5
true .

?- main.
Enter operation (+, -, *, /, mod, **, square): **
|: .
How many numbers? |: 1.
Enter number: |: 2.
Result: 2
true .

?- main.
Enter operation (+, -, *, /, mod, **, square): -
|: .
How many numbers? |: 4.
Enter number: |: 3.
Enter number: |: 4.
Enter number: |: 5.
Enter number: |: 6.
Result: -12
true .
[23bcs123@mepcolinux ex6]$cat p3.pl
CODE:
:- dynamic item/3.     % item(Name, Price, StockQty)
:- dynamic order/2.    % order(Name, OrderedQty)

% -------- Add Item to Store --------
add_item(Name, Price, Qty) :-
    assertz(item(Name, Price, Qty)),
    write('Item added to store'), nl.

% -------- Delete Item from Store --------
delete_item(Name) :-
    retractall(item(Name, _, _)),
    write('Item deleted from store'), nl.

% -------- Increase Stock --------
increase_stock(Name, Inc) :-
    retract(item(Name, Price, Qty)),
    NewQty is Qty + Inc,
    assertz(item(Name, Price, NewQty)),
    write('Stock increased'), nl.

% -------- Decrease Stock --------
decrease_stock(Name, Dec) :-
    retract(item(Name, Price, Qty)),
    NewQty is Qty - Dec,
    ( NewQty >= 0 ->
        assertz(item(Name, Price, NewQty)),
        write('Stock decreased'), nl
    ;
        write('Not enough stock'), nl,
        assertz(item(Name, Price, Qty))
    ).

% -------- Place Order --------
place_order(Name, Qty) :-
    item(Name, Price, Stock),
    Qty =< Stock,   % check stock availability
    NewStock is Stock - Qty,

    % update stock
    retract(item(Name, Price, Stock)),
    assertz(item(Name, Price, NewStock)),

    % add/update order
    ( retract(order(Name, OldQty)) ->
        NewQty is OldQty + Qty
    ;
        NewQty is Qty
    ),
    assertz(order(Name, NewQty)),

    write('Order placed'), nl.

place_order(Name, _) :-
    write('Item not available or insufficient stock'), nl.

% -------- Delete Order --------
delete_order(Name) :-
    retractall(order(Name, _)),
    write('Order removed'), nl.

% -------- Display Bill --------
display_bill :-
    write('------- CUSTOMER BILL -------'), nl,
    write('Item\tPrice\tQty\tSubtotal'), nl,
    show_orders,
    grand_total(Total),
    write('-----------------------------'), nl,
    write('Grand Total = '), write(Total), nl.

% -------- Show Ordered Items --------
show_orders :-
    order(Name, Qty),
    item(Name, Price, _),
    Subtotal is Price * Qty,
    write(Name), write('\t'),
    write(Price), write('\t'),
    write(Qty), write('\t'),
    write(Subtotal), nl,
    fail.
show_orders.

% -------- Grand Total --------
grand_total(Total) :-
    findall(Sub,
        (order(Name, Qty), item(Name, Price, _), Sub is Price*Qty),
        List),
    sum_list(List, Total).

OUTPUT:
?- add_item(rice, 50, 2).
Item added to store
true.

?- add_item(milk, 30, 3).
Item added to store
true.

?- place_order(rice, 2).
Order placed
true .

?- display_bill.
------- CUSTOMER BILL -------
Item    Price   Qty     Subtotal
rice    50      2       100
-----------------------------
Grand Total = 100
true.

?- place_order(milk, 3).
Order placed
true .

?- display_bill.
------- CUSTOMER BILL -------
Item    Price   Qty     Subtotal
rice    50      2       100
milk    30      3       90
-----------------------------
Grand Total = 190
true.

?- place_order(rice, 2).
Item not available or insufficient stock
true.

?-  add_item(rice, 50, 5).
Item added to store
true.

?- place_order(rice, 2).
Order placed
true .

?- display_bill.
------- CUSTOMER BILL -------
Item    Price   Qty     Subtotal
milk    30      3       90
rice    50      4       200
rice    50      4       200
-----------------------------
Grand Total = 490
true.
[23bcs123@mepcolinux ex6]$exit

Script done on Tue Mar 31 11:36:31 2026