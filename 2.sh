while true  
do  
  count=`ps -ef | grep "money.py" | grep -v "grep"`  
  if [ "$?" != "0" ];then  
	 sleep 140
     bash -c "python money.py"  
  else
	 echo "程序已运行！"
  fi  
  sleep 120  
done  