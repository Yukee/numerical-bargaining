# Numerical bargaining

Numerical tools for finding equilibria of bargaining games.

## Where to start?
1. Take a look at [this simple bargaining model](https://github.com/Yukee/numerical-bargaining/blob/main/simple_twoplayer_bargaining.ipynb), which walks you through the steps of creating an extensive form game and solving for the subgame perfect equilibria with Gambit.
1. [This more involved example](https://github.com/Yukee/numerical-bargaining/blob/main/threeplayer_bargaining.ipynb) features a 3-player bargaining model.
2. Run your own experiments! See below for the Gambit API installation instructions.

## Installing the Gambit python API
You'll need the Gambit python API to run the scripts in that repo.
The [official  installation instructions](https://gambitproject.readthedocs.io/en/latest/build.html#build-python) are a bit vague. 
Here's a procedure that worked for me on MacOS.

### Install Gambit from the git repo

1. `git clone` [`https://github.com/gambitproject/gambit.git`](https://github.com/gambitproject/gambit.git)
2. Navigate to gambit, run `aclocal`, `glibtoolize` (you can install it with [Brew](https://brew.sh/)), `autoconf`
3. Run `./configure`
4. Run `make`
5. Run `sudo make install`

Remark: I also tried using the [gambit-15 and gambit-16 tarballs](http://www.gambit-project.org/), but I couldn't get the python interface to run properly with those (I guess, older) versions.

### Install the python interface

1. Create a new environment `conda create -n gambit python=3 cython ipython scipy`
2. `conda activate gambit`
3. `cd [gambit git dir]/src/python`
4. `CFLAGS=-stdlib=libc++ python setup.py build`

At that step, I ran into the error described [here](https://github.com/gambitproject/gambit/issues/273#issue-950074287). The solution described [here](https://github.com/gambitproject/gambit/issues/273#issuecomment-895463705) worked for me.

5. Now we're ready for installation: run `python setup.py install`

### Fix runtime problems

I had to update the `nash.py` file (the original is [here](https://github.com/gambitproject/gambit/blob/v16.0.1/src/python/gambit/nash.py)) to run without errors on MacOS.
I've based my edits on the file given [here](https://github.com/gambitproject/gambit/pull/266#issue-516555733), but I had to modify it a bit for it to work with my version of Gambit. The file I end up using can be found in this repo, [here](https://github.com/Yukee/numerical-bargaining/blob/main/src/nash.py).

## [WIP] Open Game Engine
* I installed Stack on a Mac with an M1 chip simply using `curl -sSL https://get.haskellstack.org/ | sh`, as explained [here](https://docs.haskellstack.org/en/stable/)
* Cloning the [open game engine repo](https://github.com/CyberCat-Institute/open-game-engine)
* Running `stack run` at the root of the repo
* xcode error `xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance`
### Tutorial
* [Website tutorial](https://statebox.org/blog/compositional-game-engine/)
* 
