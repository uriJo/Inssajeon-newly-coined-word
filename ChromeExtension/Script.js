var powerOn=true;

var bubbleDOM = document.createElement('div');
bubbleDOM.setAttribute('id',"dom");
bubbleDOM.setAttribute('draggable', true);

var content = document.createElement('div');
bubbleDOM.setAttribute('class', 'selection_bubble');
document.body.appendChild(bubbleDOM);

document.getElementById('dom').setAttribute('draggable', 'true'); 

var isOn =0;
var words = []; 
var imageOn=0;
selection =''
save =''

var image = new Image();
var _graph = new Image();


chrome.storage.onChanged.addListener(function(changes, namespace) {
    if(powerOn==true){    
        powerOn=false;
        //alert(powerOn);
    }
      else{
        powerOn=true;
        //alert(powerOn);
      }
  });


  
//// 이 부분만 보면 됨, 나머지는 모양 , 기능 전용
document.addEventListener('mouseup', function (e) {
        //alert(localStorage.getItem("powerOn"));
        var selection = window.getSelection().toString();
        if (selection.length > 1){
            //var _graph = new Image();
            $.post("http://13.209.97.226:5000//search", { name: selection }, function (text) {
                output=text;
                window.getSelection().empty();
                
                $.post("http://13.209.97.226:5000//graph", { name: selection }, function (graph) {
                        _graph.src = 'data:image/png;base64,'+ graph;
                        _graph.style.width = '250px'
                        _graph.style.height = '220px'
                        _graph.id="imagecloud";
                    waitBubble(e.clientX,e.clientY,output,selection,_graph); //output의 내용을 말풍선 형태로 보여준다
            }); 
          });    
        }
        
       
}, false);


document.addEventListener('mousewheel', function (e) {
    isOn=0
}, false);


function waitBubble(mouseX, mouseY, o, s,_graph) {
    bubbleDOM.setAttribute('draggable', true);
    bubbleDOM.style.top = mouseY-10 + 'px';
    bubbleDOM.style.left = mouseX-10 + 'px';
    bubbleDOM.style.visibility = 'visible';  
    bubbleDOM.innerHTML = '<button id="gb"  class ="DOMbutton" >&nbspX&nbsp</button><br/>';
    bubbleDOM.innerHTML += '&nbsp&nbsp&nbsp<h2>" '+s+' " </h2>' + '<br>&nbsp&nbsp&nbsp<button id="gb" class ="DOMbutton" >&nbsp 검 색 &nbsp</button><br/>';
    output=o;
    selection=s;

    document.getElementsByClassName("DOMbutton")[0].addEventListener('click', function(e){ //끄기 버튼
        isOn=0;
        bubbleDOM.innerHTML=''
        bubbleDOM.style.visibility = 'hidden';
        selection=''
        output=''
        save=''
    });
    
    //var image = new Image();
    document.getElementsByClassName("DOMbutton")[1].addEventListener('click', function(e){ // 검색버튼
        document.getElementsByClassName("DOMbutton")[1].textContent=' 검색중 ... '
        $.post("http://13.209.97.226:5000//img", { name: selection }, function (data) { 
            image.src = 'data:image/png;base64,'+ data;
            image.style.width = '350px'
            image.style.height = '250px'
            image.id="imagecloud";

            renderBubble(mouseX,mouseY,output,selection,image,_graph);
            });   
        });
        

}



function renderBubble(mouseX, mouseY, output, selection ,image,_graph) { // dataset에 없는 경우 > image 없어야함
    bubbleDOM.setAttribute('draggable', true);
    isOn=1;   
    imageOn=0;
    bubbleDOM.innerHTML = '<button id="gb"  class ="DOMbutton" >&nbspX&nbsp</button><br/>';
    if(image.src=='data:image/png;base64,'){ //image ==NULL
        bubbleDOM.innerHTML += '<br><h2>" '+selection+' " </h2>';
        bubbleDOM.innerHTML+= '<br>'+output+'&nbsp&nbsp'
        bubbleDOM.innerHTML += '"'+selection+'"은(는) 인싸전에 등재되지 않았습니다.';

        document.getElementsByClassName("DOMbutton")[0].addEventListener('click', function(e){
            isOn=0;
            bubbleDOM.innerHTML=''
            bubbleDOM.style.visibility = 'hidden';
            selection=''
            output=''
            save=''
        });
    }
    else{
            bubbleDOM.innerHTML += '<br><h2>" '+selection+' " </h2>';
            bubbleDOM.innerHTML += '<br><h4> 동시 출현 단어 Wordcloud </h4>';
            bubbleDOM.appendChild(image)
            //bubbleDOM.innerHTML += output;
            
            bubbleDOM.innerHTML +='<br/><button id="gb"  class ="DOMbutton" >&nbsp예 시&nbsp</button><br/>';
            bubbleDOM.style.top = mouseY+ 'px';
            bubbleDOM.style.left = mouseX+ 'px';
            bubbleDOM.style.visibility = 'visible';  


            document.getElementsByClassName("DOMbutton")[0].addEventListener('click', function(e){
                isOn=0;
                bubbleDOM.innerHTML=''
                bubbleDOM.style.visibility = 'hidden';
                selection=''
                output=''
                save=''
            });

            document.getElementsByClassName("DOMbutton")[1].addEventListener('click', function(e){

                if(imageOn==0){
                    //bubbleDOM.appendChild(content)\
                    content.innerHTML= '<br>'+output+'&nbsp&nbsp'
                    bubbleDOM.appendChild(content)
                    bubbleDOM.appendChild(_graph)
                    document.getElementsByClassName("DOMbutton")[1].textContent=' 숨 김 '
                    imageOn=1;
                }
                else{
                    bubbleDOM.removeChild(content)
                    bubbleDOM.removeChild(_graph)
                    document.getElementsByClassName("DOMbutton")[1].textContent=' 예시 및 감성 분석 '
                    imageOn=0;
                }
                
            });
    }
    
}

bubbleDOM.ondragstart = function(event) {

    document.body.append(bubbleDOM);
    // centers the ball at (pageX, pageY) coordinates
    function moveAt(pageX, pageY) {
        bubbleDOM.style.left = pageX - bubbleDOM.offsetWidth / 2 + 'px';
        bubbleDOM.style.top = pageY - bubbleDOM.offsetHeight / 2 + 'px';
    }
  
    // move our absolutely positioned ball under the pointer
    moveAt(event.clientX, event.clientY);
  
    function ondragmove(event) {
      moveAt(event.clientX, event.clientY);
    }
  
    // (2) move the ball on mousemove
    document.addEventListener('mousemove', ondragmove);
  
    // (3) drop the ball, remove unneeded handlers
    bubbleDOM.onmouseup = function() {
      document.removeEventListener('mousemove', ondragmove);
      bubbleDOM.onmouseup = null;
    };
    
  };