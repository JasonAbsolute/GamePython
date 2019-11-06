// Distance map
PImage map;
int nxt = 0;
int nr = 3200;
int nc = 2700;

void setup ()
{
  size (3200, 2700);
  map = loadImage  ("shadowc.png");
}

void draw ()
{
 color c;
 int cc, cr;
 
  cc = 0;
  for (int i=1; i<nr; i++)
  {
    for (int j=1; j<nc; j++)
    {
      c = get1 (map, i,j);         // Get the pixel value
      if (c == 255)                // White pixel?
      {                           // Check all neighbors
        cr = get1(map, i+1, j);  // to see if any have a
        if (cr == nxt)           // have the 'nxt' value
        {
          set2 (map, i, j, nxt+1); cc++;
          if (get2(map,i,j)!=nxt+1) println ("error.");
          continue;
        }
        
        cr = get1 (map, i-1, j);    
        if (cr == nxt)             
        {
          set2 (map, i,j, nxt+1); cc++;
          if (get2(map,i,j)!=nxt+1) println ("error.");
          continue;
        }
        
        cr = get1 (map, i, j+1);   
        if (cr == nxt)   
        {
          set2 (map, i,j, nxt+1);   cc++;       
          if (get2(map,i,j)!=nxt+1) println ("error.");
          continue;
        }   
        
        cr = get1 (map, i, j-1);   
        if (cr == nxt)   
        {
          set2 (map, i,j, nxt+1);    cc++;
          if (get2(map,i,j)!=nxt+1) println ("error.");
          continue;
        }
        set2 (map, i, j, c);
      }  // if c == 255
    }
  }
  println (cc, " Pixels changed.");
  if (cc == 0) 
  {
    image (map, 0, 0);
    println ("Stopping.");
    noLoop();
  }
  
  for (int i=1; i<nc; i++)
  {
    for (int j=1; j<nr; j++)
    {
      cr = get2 (map, i,j);
      set1 (map, i,j, cr);
      if (get2(map,i,j)!=cr) println ("error.");
    }
  }
  
  image(map, 0, 0);
  nxt = nxt + 1;
  if (nxt >= 255)
  {
    noLoop ();
    println ("Stopping ", nxt);
    map.save ("dist.png");
  }
  println (nxt);
//  map.save (""+str(nxt)+".png");
}

int get1 (PImage im, int i, int j)
{
  color c;
  
  c = im.get (i,j);
  return (int)red(c);
}

int get2 (PImage im, int i, int j)
{
  color c;
  
  c = im.get (i,j);
  return (int)green(c);
}

void set1 (PImage im, int i, int j, int val)
{
  color c1;
  c1 = im.get(i,j);
  im.set (i, j, color(val, (int)green(c1), val));
}

void set2 (PImage im, int i, int j, int val)
{
  color c1;
  c1 = im.get(i,j);
  im.set (i, j, color((int)red(c1), val, val));
}
