# parsimony

Hello, stranger! This repository contains papers, tools, and documentation related to the study of parsimonious Turing machine generation. This project's only dependency is on Python 2.7, although in order to clone the repository you will also need to have Git.

At the highest level, we have Laconic, which is a language designed to be easily usable without any specialized knowledge of Turing machines. To find documentation explaining how Laconic works and how to use it, navigate to: 

```
parsimony/src/laconic/
```

and read ```laconic_quick_start.pdf``` or ```laconic_readme.pdf```, respectively. This is the recommended approach for somebody who just wants to get started making Turing machines as quickly as possible. ```laconic_ops.pdf``` provides an exhaustive list of Laconic primitives. Watch out--most of them are intuitive, but not all!

For a reader who wants to understand the compilation algorithm in its entirely, or who wants to work at a lower level in the hopes of making even more parsimonious Turing machines, it is a good idea to understand TMD. ```laconic_to_tmd.pdf``` (found in the ```laconic``` directory) explains the Laconic-to-TMD compilation process. To understand how TMD works and learn how to use it, navigate to:

```
parsimony/src/tmd/
```

and read ```tmd_doc.pdf``` or ```tmd_readme.pdf```, respectively. ```tmd_to_tm.pdf``` explains the TMD-to-Turing-Machine compilation process. 

Finally, to run and understand the Turing machine's you've generated, you'll need to navigate to:

```
parsimony/src/tm/
```

There, you'll find ```tm_readme.pdf```, which will explain how to run the Turing machines, ```tm_parse.pdf```, which explains how to read your Turing machines, ```tm_def.pdf```, which gives formal definitions for the Turing machines I use, and ```tm_doc.pdf```, which explains how the Turing machines work.

All of the documentation referenced here can also be found at:

```
parsimony/tex/docs/
```

along with the LaTeX source used to generate it. In particular, if you are looking through the repository using a browser, you'll only be able to see the pdfs themselves by going to the ```docs``` directory (the locations I described above actually point to symlinks).

My research paper which presents results about the Busy Beaver function using the tools in this repository can be found at: 

```
parsimony/tex/busybeaver/busybeaver.pdf
```

Happy Turing machining!