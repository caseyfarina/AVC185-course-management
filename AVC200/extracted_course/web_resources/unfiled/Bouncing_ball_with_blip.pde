void setup() {
  size(200,200);
  background(0);
  smooth();
  frameRate(30);
}


int x = 0;
// location of the circle
int y = 0;
// y location of the circle
int x_speed = 19;
// speed in the x direction
int y_speed = 7;
//speed in the ydirection
int size = 20;

void draw() {
  background(0);
  ellipse(x,y,size,size);
  
  if (x > width) {
    x_speed = x_speed*(-1);
    size = 80;
   }
   
   if (x < 0) {
     x_speed = x_speed*(-1);
   }
   
     if (y > height) {
    y_speed = y_speed*(-1);
   }
   
   if (y < 0) {
     y_speed = y_speed*(-1);
   }
   
   if (x > width) {
     size = 80;
   } else {
     size = 20;
   }
   
    if (x < 0) {
     size = 80;
   }  
   
   if (y > height) {
     size = 80;
   } 
   
    if (y < 0) {
     size = 80;
   } 
  x = x + x_speed;
  y = y + y_speed;
  
}



