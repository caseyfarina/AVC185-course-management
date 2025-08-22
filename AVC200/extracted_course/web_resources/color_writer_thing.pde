void setup() {
  size(1000,1000);
  colorMode(HSB, float(width));
  background(width,width,0);
  smooth();
}

void draw() {
  colorMode(HSB, float(width));
  strokeWeight(abs(pmouseX-mouseX));
  stroke(float(mouseX),float(width),float(width/1),width/2);
  line(pmouseX,pmouseY,mouseX,mouseY);
  strokeWeight(2);
  fill(mouseX+random(-500.0,500.0),float(width),float(width/1),width/2);
  ellipse(mouseX,mouseY,(abs(pmouseX-mouseX)),(abs(pmouseX-mouseX)));
  ellipse(mouseX+(random(-(width/020),(width/20))),mouseY+(random(-(width/20),(width/20))),(abs(pmouseX-mouseX)),(abs(pmouseX-mouseX)));
  
}
  
  void keyPressed () {
    background(width,width,0);
    ellipse(mouseX,mouseY,(abs(pmouseX-mouseX)),(abs(pmouseX-mouseX)));
  }
  
  void mousePressed () {
    rect(mouseX+(random(-(width/020),(width/20))),mouseY+(random(-(width/20),(width/20))),random(width/4),random(width/4));
  }
