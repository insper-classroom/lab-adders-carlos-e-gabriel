#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    """Meio somador de 1 bit.

    Args:
        a: Entrada de 1 bit.
        b: Entrada de 1 bit.
        soma: Saida de soma.
        carry: Saida de carry.
    """
    @always_comb
    def comb():
        soma.next = a ^ b 
        carry.next = a and b

    return instances()

@block
def fullAdder(a, b, c, soma, carry):
    s1 = Signal(bool(0)) # (1)
    s2 = Signal(bool(0)) 
    s3 = Signal(bool(0))

    half_1 = halfAdder(a, b, s1, s2) 
    half_2 = halfAdder(c, s1, soma, s3) 

    @always_comb
    def comb():
        carry.next = s2 | s3 

    return instances()


@block
def adder2bits(x, y, soma, carry):
    """Somador de 2 bits.

    Implementacao esperada com dois full adders,
    gerando uma soma de 2 bits e carry final.

    Args:
        x: Vetor de entrada de 2 bits. 
        y: Vetor de entrada de 2 bits. 
        soma: Vetor de saida de 2 bits.
        carry: Carry de saida.
    """

    c0 = Signal(bool(0))
    fa0 = fullAdder(
        a=x[0],
        b=y[0],
        c=Signal(bool(0)),  
        soma=soma[0],
        carry=c0
    )
    fa1 = fullAdder(
        a=x[1],
        b=y[1],
        c=c0,
        soma=soma[1],
        carry=carry
    )

    return instances()



@block
def adder(x, y, soma, carry):

    n = len(x)

    carries = [Signal(bool(0)) for _ in range(n + 1)]

    fas = []

    for i in range(n):
        fa = fullAdder(
            x[i],
            y[i],
            carries[i],      
            soma[i],
            carries[i+1]    
        )
        fas.append(fa)

    @always_comb
    def assign():
        carry.next = carries[n]

    return fas, assign


@block
def addervb(x, y, soma, carry):

    n = len(x)
    mask = (1 << n) - 1

    @always_comb
    def comb():
        total = int(x) + int(y)

        soma.next = total & mask
        carry.next = bool((total >> n) & 1)

    return comb