# GitHub Cheatsheet

![](../../git/files/images/gitCheatsheet.jpg)


```sh
git status
git add .
git commit
git push

git clone 

git pull

git set remote -v 
git remote -v

Create new branch:
git checkout -b name

Switching between branches
git checkout master

git pull upstream master

git submodule deinit -f . 

git stash
```


```sh
usage: git [-v | --version] [-h | --help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           [--super-prefix=<path>] [--config-env=<name>=<envvar>]
           <command> [<args>]

These are common Git commands used in various situations:

start a working area (see also: git help tutorial)
   clone     Clone a repository into a new directory
   init      Create an empty Git repository or reinitialize an existing one

work on the current change (see also: git help everyday)
   add       Add file contents to the index
   mv        Move or rename a file, a directory, or a symlink
   restore   Restore working tree files
   rm        Remove files from the working tree and from the index

examine the history and state (see also: git help revisions)
   bisect    Use binary search to find the commit that introduced a bug
   diff      Show changes between commits, commit and working tree, etc
   grep      Print lines matching a pattern
   log       Show commit logs
   show      Show various types of objects
   status    Show the working tree status

grow, mark and tweak your common history
   branch    List, create, or delete branches
   commit    Record changes to the repository
   merge     Join two or more development histories together
   rebase    Reapply commits on top of another base tip
   reset     Reset current HEAD to the specified state
   switch    Switch branches
   tag       Create, list, delete or verify a tag object signed with GPG

collaborate (see also: git help workflows)
   fetch     Download objects and refs from another repository
   pull      Fetch from and integrate with another repository or a local branch
   push      Update remote refs along with associated objects
```


![](../git/images/gitCheat.jpg)

```sh
vi ~/.gitconfig
```

```yml
[user]
	name = Julian Wendland
	email = julianwendland@gmx.de
	username = julianwe
[init]
	defaultBranch = master
[core]
	editor = nvim
	whitespace = fix,-indent-with-non-tab,trailing-space,cr-at-eol
	pager = delta
[sendemail]
	smtpencryption = tls
	smtpserver = smtp.gmail.com
	smtpuser = julianwendland@gmx.de
	smtppass = password
	smtpserverport = 587
[web]
	browser = google-chrome
[instaweb]
	httpd = apache2 -f
[rerere]
	enabled = 1
	autoupdate = 1
[color]
	ui = auto
[color "branch"]
	current = yellow bold
	local = cyan bold
	remote = green bold
[color "diff"]
	meta = cyan bold
	frag = magenta bold
	old = red bold
	new = green bold
	whitespace = white bold
[color "status"]
	added = green bold
	changed = blue bold
	untracked = cyan bold
[diff]
	tool = vimdiff
[difftool]
	prompt = false
[delta]
	features = line-numbers decorations
	line-numbers = true
[delta "decorations"]
	minus-style = red bold normal
	plus-style = green bold normal
	minus-emph-style = white bold red
	minus-non-emph-style = red bold normal
	plus-emph-style = white bold green
	plus-non-emph-style = green bold normal
	file-style = yellow bold none
	file-decoration-style = yellow box
	hunk-header-style = magenta bold
	hunk-header-decoration-style = magenta box
	minus-empty-line-marker-style = normal normal
	plus-empty-line-marker-style = normal normal
	line-numbers-right-format = "{np:^4}│ "
[github]
	user = julianwe
	token = token
[gitflow "prefix"]
	versiontag = v
[sequence]
	editor = interactive-rebase-tool
[alias]
	a = add --all
	ai = add -i
	#############
	ap = apply
	as = apply --stat
	ac = apply --check
	#############
	ama = am --abort
	amr = am --resolved
	ams = am --skip
	#############
	b = branch
	ba = branch -a
	bd = branch -d
	bdd = branch -D
	br = branch -r
	bc = rev-parse --abbrev-ref HEAD
	bu = !git rev-parse --abbrev-ref --symbolic-full-name "@{u}"
	bs = !git-branch-status
	#############
	c = commit
	ca = commit -a
	cm = commit -m
	cam = commit -am
	cem = commit --allow-empty -m
	cd = commit --amend
	cad = commit -a --amend
	ced = commit --allow-empty --amend
	#############
	cl = clone
	cld = clone --depth 1
	clg = !sh -c 'git clone https://github.com/$1 $(basename $1)' -
	clgp = !sh -c 'git clone git@github.com:$1 $(basename $1)' -
	clgu = !sh -c 'git clone git@github.com:$(git config --get user.username)/$1 $1' -
	#############
	cp = cherry-pick
	cpa = cherry-pick --abort
	cpc = cherry-pick --continue
	#############
	d = diff
	dp = diff --patience
	dc = diff --cached
	dk = diff --check
	dck = diff --cached --check
	dt = difftool
	dct = difftool --cached
	#############
	f = fetch
	fo = fetch origin
	fu = fetch upstream
	#############
	fp = format-patch
	#############
	fk = fsck
	#############
	g = grep -p
	#############
	l = log --oneline
	lg = log --oneline --graph --decorate
	#############
	ls = ls-files
	lsf = !git ls-files | grep -i
	#############
	m = merge
	ma = merge --abort
	mc = merge --continue
	ms = merge --skip
	#############
	o = checkout
	om = checkout master
	ob = checkout -b
	opr = !sh -c 'git fo pull/$1/head:pr-$1 && git o pr-$1'
	#############
	pr = prune -v
	#############
	ps = push
	psf = push -f
	psu = push -u
	pst = push --tags
	#############
	pso = push origin
	psao = push --all origin
	psfo = push -f origin
	psuo = push -u origin
	#############
	psom = push origin master
	psaom = push --all origin master
	psfom = push -f origin master
	psuom = push -u origin master
	psoc = !git push origin $(git bc)
	psaoc = !git push --all origin $(git bc)
	psfoc = !git push -f origin $(git bc)
	psuoc = !git push -u origin $(git bc)
	psdc = !git push origin :$(git bc)
	#############
	pl = pull
	pb = pull --rebase
	#############
	plo = pull origin
	pbo = pull --rebase origin
	plom = pull origin master
	ploc = !git pull origin $(git bc)
	pbom = pull --rebase origin master
	pboc = !git pull --rebase origin $(git bc)
	#############
	plu = pull upstream
	plum = pull upstream master
	pluc = !git pull upstream $(git bc)
	pbum = pull --rebase upstream master
	pbuc = !git pull --rebase upstream $(git bc)
	#############
	rb = rebase
	rba = rebase --abort
	rbc = rebase --continue
	rbi = rebase --interactive
	rbs = rebase --skip
	#############
	re = reset
	rh = reset HEAD
	reh = reset --hard
	rem = reset --mixed
	res = reset --soft
	rehh = reset --hard HEAD
	remh = reset --mixed HEAD
	resh = reset --soft HEAD
	rehom = reset --hard origin/master
	#############
	r = remote
	ra = remote add
	rr = remote rm
	rv = remote -v
	rn = remote rename
	rp = remote prune
	rs = remote show
	rao = remote add origin
	rau = remote add upstream
	rro = remote remove origin
	rru = remote remove upstream
	rso = remote show origin
	rsu = remote show upstream
	rpo = remote prune origin
	rpu = remote prune upstream
	#############
	rmf = rm -f
	rmrf = rm -r -f
	#############
	s = status
	sb = status -s -b
	#############
	sa = stash apply
	sc = stash clear
	sd = stash drop
	sl = stash list
	sp = stash pop
	ss = stash save
	ssk = stash save -k
	sw = stash show
	st = !git stash list | wc -l 2>/dev/null | grep -oEi '[0-9][0-9]*'
	#############
	t = tag
	td = tag -d
	#############
	w = show
	wp = show -p
	wr = show -p --no-color
	#############
	svnr = svn rebase
	svnd = svn dcommit
	svnl = svn log --oneline --show-commit
	#############
	subadd = !sh -c 'git submodule add git://github.com/$1 $2/$(basename $1)' -
	subrm = !sh -c 'git submodule deinit -f -- $1 && rm -rf .git/modules/$1 && git rm -f $1' -
	subup = submodule update --init --recursive
	subpull = submodule foreach 'git pull --tags -f origin master || git pull --tags -f origin main'
	#############
	assume = update-index --assume-unchanged
	unassume = update-index --no-assume-unchanged
	assumed = !git ls -v | grep ^h | cut -c 3-
	unassumeall = !git assumed | xargs git unassume
	assumeall = !git status -s | awk {'print $2'} | xargs git assume
	#############
	bump = !sh -c 'git commit -am \"Version bump v$1\" && git psuoc && git release $1' -
	release = !sh -c 'git tag v$1 && git pst' -
	unrelease = !sh -c 'git tag -d v$1 && git pso :v$1' -
	merged = !sh -c 'git o master && git plom && git bd $1 && git rpo' -
	aliases = !git config -l | grep alias | cut -c 7-
	snap = !git stash save 'snapshot: $(date)' && git stash apply 'stash@{0}'
	bare = !sh -c 'git symbolic-ref HEAD refs/heads/$1 && git rm --cached -r . && git clean -xfd' -
	whois = !sh -c 'git log -i -1 --author=\"$1\" --pretty=\"format:%an <%ae>\"' -
	serve = daemon --reuseaddr --verbose --base-path=. --export-all ./.git
	#############
	behind = !git rev-list --left-only --count $(git bu)...HEAD
	ahead = !git rev-list --right-only --count $(git bu)...HEAD
	#############
	ours = "!f() { git checkout --ours $@ && git add $@; }; f"
	theirs = "!f() { git checkout --theirs $@ && git add $@; }; f"
	subrepo = !sh -c 'git filter-branch --prune-empty --subdirectory-filter $1 master' -
	human = name-rev --name-only --refs=refs/heads/*

```


**Install [GitHub CLI](https://cli.github.com/)**

```sh
brew install gh

Work seamlessly with GitHub from the command line.

USAGE
  gh <command> <subcommand> [flags]

CORE COMMANDS
  auth:        Authenticate gh and git with GitHub
  browse:      Open the repository in the browser
  codespace:   Connect to and manage codespaces
  gist:        Manage gists
  issue:       Manage issues
  org:         Manage organizations
  pr:          Manage pull requests
  project:     Work with GitHub Projects.
  release:     Manage releases
  repo:        Manage repositories

GITHUB ACTIONS COMMANDS
  cache:       Manage Github Actions caches
  run:         View details about workflow runs
  workflow:    View details about GitHub Actions workflows

ALIAS COMMANDS
  co:          Alias for "pr checkout"

ADDITIONAL COMMANDS
  alias:       Create command shortcuts
  api:         Make an authenticated GitHub API request
  completion:  Generate shell completion scripts
  config:      Manage configuration for gh
  extension:   Manage gh extensions
  gpg-key:     Manage GPG keys
  label:       Manage labels
  ruleset:     View info about repo rulesets
  search:      Search for repositories, issues, and pull requests
  secret:      Manage GitHub secrets
  ssh-key:     Manage SSH keys
  status:      Print information about relevant issues, pull requests, and notifications across repositories
  variable:    Manage GitHub Actions variables

HELP TOPICS
  actions:     Learn about working with GitHub Actions
  environment: Environment variables that can be used with gh
  exit-codes:  Exit codes used by gh
  formatting:  Formatting options for JSON data exported from gh
  mintty:      Information about using gh with MinTTY
  reference:   A comprehensive reference of all gh commands

FLAGS
  --help      Show help for command
  --version   Show gh version

EXAMPLES
  $ gh issue create
  $ gh repo clone cli/cli
  $ gh pr checkout 321

LEARN MORE
  Use 'gh <command> <subcommand> --help' for more information about a command.
  Read the manual at https://cli.github.com/manual

```

**Examples**

```sh

gh auth login 

gh issue list

gh issue create --title "I found a bug" --body "Nothing works"

gh api repos/JulianWe/julianwe.github.io/issues/2/comments -f body='Hi from CLI'

```