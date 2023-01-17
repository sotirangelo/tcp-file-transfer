# Python TCP file transfer

Repository for the third assignment of the _Wireless Networks and Mobile Communications_ course offered by the [Department of Informatics](https://www.dept.aueb.gr/en/cs) of the [Athens University of Economics and Business](https://www.aueb.gr/en).

> **Students** <br>
>
> Sotirios Angelos Angelopoulos <br>
> t8190001 <br>
> Department of Management Science and Technology <br>
> Athens University of Economics and Business <br> > sotiraggelos@gmail.com
>
> Ioanna Moraiti <br>
> t8190121 <br>
> Department of Management Science and Technology<br>
> Athens University of Economics and Business <br> > joannamoraiti1@gmail.com
>
> **Supervising Professor**
>
> Vasilios Siris, Professor <br>
> Deparment of Informatics <br>
> Athens University of Economics and Business <br> > vsiris@aueb.gr

<hr>

## Overview

A detailed description of the assignment is available in Greek [here](ADKE_Ergasia3_2022.pdf).
The purpose of this assignment is to carry out experiments of transferring files from two servers to a single client. In order to conduct these experiments, students are expected to develop both a server and a client for transferring a total of 160 m4s files (available [here](server_data/)).

While the experiments themselves are not present in this repository, the implementations of the both the server and the client are made available here.

## Requirements

-   [Python 3.10](https://www.python.org/downloads/release/python-3109/)

-   Exactly 2 instances of [server.py](server.py) running

## Implementation

The language we chose for this assignment was _Python_. While socket programming in _Python_ is similar to other languages, its standard library includes the higher-level module called `socket`, that provides a more user-friendly interface for working with sockets. Adding that to _Python_'s high-level nature, it was a more convenient choice for rapid development and prototyping.

While the server's implementation is pretty straightforward, the client is a bit more complex, as expected from the assignment's description. It is the client's responsibility to make sequential request for files, at the same time for each server. For concurrency in the client's requests, we made use of the `asyncio` module included in the standard library.
