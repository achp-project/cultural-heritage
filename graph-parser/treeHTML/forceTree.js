/*
Based on code found in https://jsfiddle.net/sheilak/9wvmL8q8/
*/

// TODO Check https://d3-graph-gallery.com/graph/interactivity_zoom.html and try to get zoom to work

var width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
var height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

var svg = d3.select("body").append("svg")
//.attr("viewBox", [0, 0, width, height])
    .attr("width", width)
    .attr("height", height);
/*
svg.call(d3.zoom()
      .extent([[0, 0], [width, height]])
      .scaleExtent([1, 8])
      .on("zoom", zoomed));

  function zoomed({transform}) {
    g.attr("transform", transform);
    debug.log("ZOOMED")
  }
*/
var force = d3.layout.force()
  .size([width, height])
  //gravity(0.2)
  .linkDistance(height / 6)
  .charge(function(node) {
    if (node.type !== 'ORG') return -2000;
    return -30;
  });

// build the arrow.
svg.append("svg:defs").selectAll("marker")
  .data(["end"]) // Different link/path types can be defined here
  .enter().append("svg:marker") // This section adds in the arrows
  .attr("id", function(d) {
    return d;
  })
  .attr("viewBox", "0 -5 10 10")
  .attr("refX", 12)
  .attr("refY", 0)
  .attr("markerWidth", 9)
  .attr("markerHeight", 5)
  .attr("orient", "auto")
  .attr("class", "arrow")
  .append("svg:path")
  .attr("d", "M0,-5L10,0L0,5");

  var json = dataset;

  var edges = [];
  json.edges.forEach(function(e) {
    var sourceNode = json.nodes.filter(function(n) {
        return n.id === e.from;
      })[0],
      targetNode = json.nodes.filter(function(n) {
        return n.id === e.to;
      })[0];

    edges.push({
      source: sourceNode,
      target: targetNode,
      value: e.Value
    });
  });

  for(var i=0; i<json.nodes.length; i++) {
    json.nodes[i].collapsing = 0;
    json.nodes[i].collapsed = false;
  }

  var link = svg.selectAll(".link");
  var node = svg.selectAll(".node");

  force.on("tick", function() {
    // make sure the nodes do not overlap the arrows
    link.attr("d", function(d) {
      // Total difference in x and y from source to target
      diffX = d.target.x - d.source.x;
      diffY = d.target.y - d.source.y;

      // Length of path from center of source node to center of target node
      pathLength = Math.sqrt((diffX * diffX) + (diffY * diffY));

      // x and y distances from center to outside edge of target node
      offsetX = (diffX * d.target.radius) / pathLength;
      offsetY = (diffY * d.target.radius) / pathLength;

      return "M" + d.source.x + "," + d.source.y + "L" + (d.target.x - offsetX) + "," + (d.target.y - offsetY);
    });

    node.attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")";
    });
  });

update();

function update(){
  var nodes = json.nodes.filter(function(d) {
    return d.collapsing == 0;
  });

  var links = edges.filter(function(d) {
    return d.source.collapsing == 0 && d.target.collapsing == 0;
  });

  force
    .nodes(nodes)
    .links(links)
    .start();

  link = link.data(links)
  
  link.exit().remove();
  
  link.enter().append("path")
    .attr("class", "link")
    .attr("marker-end", "url(#end)");

  node = node.data(nodes);
  
  node.exit().remove();
  
  node.enter().append("g")
    .attr("class", function(d) {
      return "node " + d.type
    });

  node.append("circle")
    .attr("class", "circle")
    .attr("r", function(d) {
      d.radius = 30;
      return d.radius
    }); // return a radius for path to use 

  node.append("text")
    .attr("x", 0)
    .attr("dy", ".35em")
    .attr("text-anchor", "middle")
    .attr("class", "text")
    .text(function(d) {
      return d.type
    });
    
  // On node hover, examine the links to see if their
  // source or target properties match the hovered node.
  node.on('mouseover', function(d) {
    link.attr('class', function(l) {
      if (d === l.source || d === l.target)
        return "link active";
      else
        return "link inactive";
    });
  });
  
  // Set the stroke width back to normal when mouse leaves the node.
  node.on('mouseout', function() {
    link.attr('class', "link");
  })
  .on('click', click);
  
  function click(d) {
    if (!d3.event.defaultPrevented) {
      var inc = d.collapsed ? -1 : 1;
      recurse(d);

      function recurse(sourceNode){
        //check if link is from this node, and if so, collapse
        edges.forEach(function(l) {
          if (l.source.id === sourceNode.id){
            l.target.collapsing += inc;
                        recurse(l.target);
          }
        });
      }
      d.collapsed = !d.collapsed;
    }      
    update();
  }
}
  
