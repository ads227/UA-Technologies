var count = 0;

function addDep() {
  var target = document.getElementById("deps")
  var e = document.getElementById("sel")
  var val = e.value;
  target.innerHTML += "<label for=\"rev\" id=\"" + count + "\"> " + val + " Revenue from event: </label><input type=\"text\" name=\"" + val + "\" id=\"" + count + "\">" + "<button id=\"" + count + "\"type=\"button\" onclick=\"rmDep(" + count + ")\">Remove</button>" + "<br id=\"" + count +  "\">" + "<br id=\"" + count +  "\">"
  count += 1;
}

function rmDep(num) {
  var element;
  while(element = document.getElementById(num)) {
    element.parentNode.removeChild(element);
  }
}
