
void setup() {
background(255,255,0);
//changes background color to yellow = red + green
size(900,500);
// changes the size of the window
rectMode(CENTER);
}

color base_color = color(100,23,200);
color accent_color = color(200,40,70);
float spread = 0.1;
//changes the rectangle anchor point to the center rather than the upper left

void draw()  {
// background(255,255,0);  



stroke(accent_color);
fill(base_color);
strokeWeight(40);
rect(width*(.5-spread),height*(.5-spread),width/4,height/4);
// this locates a rectagle at one quarter width and height
rect(width*(.5+spread),height*(.5+spread),width/4,height/4);
fill(base_color);
stroke(accent_color);
strokeWeight(20);
ellipse(width*(.5+spread),height*(.5-spread),width/4,height/4);
ellipse(width*(.5-spread),height*(.5+spread),width/4,height/4);
spread = (mouseX*.005);
};

