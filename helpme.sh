#!/bin/bash
QH_APP_TAG=quickhost
PROFILE=quickhost-root

function listem() {
  function _listall() {
    #aws --profile "$PROFILE" --region "us-east-1" ec2 describe-instances \
    aws ec2 describe-instances \
      --filters "Name=tag-key,Values=${QH_APP_TAG}" \
      --query 'Reservations[].Instances[].{ID:InstanceId,STATE:State.Name}' \
      --output text
    return
  }
  function _listrunning() {
    aws ec2 describe-instances \
      --filters 'Name=instance-state-name,Values=running' "Name=tag-key,Values=${QH_APP_TAG}" \
      --query 'Reservations[].Instances[].InstanceId' \
      --output text
    return
  }
  case "$1" in 
    -r|--running) _listrunning ;;
    -h|--help) echo "listem            get all instances tagged with '${QH_APP_TAG}'

      [-r|--running]    show only running instances (for debugging)
      [-h|--help]       show this dialog and exit
      ";;
    *) _listall ;;
  esac
}

function blog () {
  local blogfile
  blogfile="${PWD}/blog/blog-$(date -I).md"
  function _template(){
    [ -f "$blogfile" ] && vim "$blogfile" && exit
    cat <<EOF > "$blogfile"
# $(date '+%A, %D')

EOF
    vim "$blogfile"
  }
  case "$1" in 
    -h|--help) echo "
      blog            write a blog post for today
      -h|--help         show this dialog and exit
      ";;
    *) _template;;
  esac

}

function sgids(){
  aws ec2 describe-security-groups \
    --filters "Name=tag-key,Values=${QH_APP_TAG}" \
    --query 'SecurityGroups[].{NAME:GroupName,ID:GroupId}'
}

function test_stuff(){
  for provider in {aws,null}; do
    for action in {make,destroy,update,init,describe}; do 
      main.py "$provider" "$action" -h
    done
  done
  main.py -h
}

case "$1" in
  list) shift; listem "$@";;
  sgs) shift; sgids "$@";;
  blog) shift; blog "$@";;
  test-help) test_stuff;;
  *) echo '
    usage:

    list            list instances
    sgs             list security groups
    blog            write a blog post for today
    test-help       print help for all of the plugin options
    help            show this dialog and exit
';;

esac
