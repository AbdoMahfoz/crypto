#!/bin/bash

run_cmd(){
	file=$(mktemp)
	$@ &> $file
	res=$?
	out=$(cat $file)
	rm $file
	if (( $res != 0 )); then
		echo "-->Error occured"
		echo "$out"
		exit
	fi
}

cur_branch=$(git branch | grep -oP "(?<=\* )\S+")
if [[ $cur_branch != "master" ]]; then
	echo "-->Was in $cur_branch, jumping to master"
	run_cmd git checkout master
else
	echo "-->Already in master"
fi
echo "-->Updating master"
run_cmd git pull origin master
run_cmd git push origin master
echo "-->Getting latest version of deploy branch"
run_cmd git branch -D deploy
run_cmd git fetch origin
run_cmd git checkout deploy
echo "-->Rebasing deploy into master"
run_cmd git rebase master
echo "-->Pushing changes"
run_cmd git push -f origin deploy
echo "-->Returning to branch $cur_branch"
run_cmd git checkout $cur_branch
