
float y;
float water_speed;

float x;
float x_speed;

void setup(){
  size(1280,720,P2D);

 y = 0;//initialize
  noStroke();
  water_speed = 6;
  x_speed = 8;
}

void draw(){
  fill(0,0,0,3);
  rect(0,0,width,height);

  fill(255);
  for(int i = 0; i < 10;i++){
    
    fill(random(20)+220);
    float upThing;
    upThing = y+random(-4,4);
    
    ellipse(
      (i*(random(20)+20))+random(-20,20)+x,
      upThing,
      random(20)+20,
      random(20)+20);
  }
  
  y+=water_speed;
  x+=x_speed;
  
  if(y > height){
    y = 0;
    water_speed = random(10);
  }
  
  if(x > width || x < 0){
    x_speed = x_speed*-1;
  }
}