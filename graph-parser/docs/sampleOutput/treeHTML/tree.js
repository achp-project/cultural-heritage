 var tree = document.querySelectorAll('ul.tree a:not(:last-child)');
 function expandNode(e) {
            e.preventDefault();
            var parent = e.target.parentElement;
            var classList = parent.classList;
            if(classList.contains("open")) {
              classList.remove('open');
              var opensubs = parent.querySelectorAll(':scope .open');
              for(var i = 0; i < opensubs.length; i++){
                  opensubs[i].classList.remove('open');
              }
            } else {
              classList.add('open');
            }
      }

function openOutlink(clickData){
    window.open(clickData['attributes']['outlink']['nodeValue']);
}

  for(var i = 0; i < tree.length; i++){
      tree[i].addEventListener('contextmenu', expandNode);
      tree[i].addEventListener('oncontextmenu', expandNode);
  }