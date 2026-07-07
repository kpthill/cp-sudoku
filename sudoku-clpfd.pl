:- use_module(library(clpfd)).

% Using <https://www.swi-prolog.org/pldoc/man?section=clpfd-sudoku>.

% ?- problem(2, Board), sudoku(Board), append(Board, Vs), label(Vs), board_display(Board).

sudoku(Rows) :-
        length(Rows, 9), maplist(same_length(Rows), Rows),
        append(Rows, Vs), Vs ins 1..9,
        maplist(all_distinct, Rows),
        transpose(Rows, Columns),
        maplist(all_distinct, Columns),
        Rows = [As,Bs,Cs,Ds,Es,Fs,Gs,Hs,Is],
        blocks(As, Bs, Cs),
        blocks(Ds, Es, Fs),
        blocks(Gs, Hs, Is).

blocks([], [], []).
blocks([N1,N2,N3|Ns1], [N4,N5,N6|Ns2], [N7,N8,N9|Ns3]) :-
        all_distinct([N1,N2,N3,N4,N5,N6,N7,N8,N9]),
        blocks(Ns1, Ns2, Ns3).

problem(1, [[_,_,_,_,_,_,_,_,_],
            [_,_,_,_,_,3,_,8,5],
            [_,_,1,_,2,_,_,_,_],
            [_,_,_,5,_,7,_,_,_],
            [_,_,4,_,_,_,1,_,_],
            [_,9,_,_,_,_,_,_,_],
            [5,_,_,_,_,_,_,7,3],
            [_,_,2,_,1,_,_,_,_],
            [_,_,_,_,4,_,_,_,9]]).

problem(2, [
	[2,_,_,_,_,_,3,_,_],
	[_,6,_,_,7,_,_,8,4],
	[_,3,_,5,_,_,2,_,9],
	[_,_,_,1,_,5,4,_,8],
	[_,_,_,_,_,_,_,_,_],
	[4,_,2,7,_,6,_,_,_],
	[3,_,1,_,_,7,_,4,_],
	[7,2,_,_,4,_,_,6,_],
	[_,_,4,_,1,_,_,_,3]]
).

board_display(Board) :-
	 maplist([R] >> format('~q~n', [R]), Board).
