function tip(){
	var bill = document.getElementById("bill");
	var billValue = bill.value;



	var percent = document.getElementsByName("tip");
	var percentValue = 1;

	for(i = 0; i < percent.length; i++){
		if(percent[i].checked){
			percentValue = percent[i].value;
		}
	}

	var total = billValue * percentValue;
	total = Math.round(total * 100) / 100;
  	total = total.toFixed(2);

	document.getElementById("out").innerHTML = total;
}

document.getElementById("submit").onclick = function() {
  tip();
};