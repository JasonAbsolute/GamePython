PImage im;


void setup ()
{
  im = loadImage ("wakes2.bmp");
  size (167, 314);
} 

void draw ()
{
  color p;
  int r, g, b, h;
  color back = color (36, 173, 171);
  float d;
  
  image (im, 0, 0);
  for (int i=0; i<167; i++)
     for (int j=0; j<314; j++)
     {
       p = im.get (i,j);
       d = distance (p, back);
       d = (int)((d/220)*255);
       im.set (i, j, color (red(p), green(p), blue(p),d));
     }
     image (im, 0, 0);
     noLoop();
     save ("xx.gif");
}

float distance (color c1, color c2)
{
  float x, y, z, d;
  
  x = red(c1)-red(c2);
  y = green(c1)-green(c2);
  z = blue(c1) - blue(c2);
  d = sqrt (x*x + y*y + z*z);
  println (d);
  return d;
}
  
