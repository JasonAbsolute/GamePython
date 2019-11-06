// Distance map
PImage map;
PImage f;
int nxt = 0;
int nr = 3200;
int nc = 2700;

void setup ()
{
  PImage t;
  size (3200, 2700);
  map = loadImage  ("xx.png");
  f = loadImage ("flags.png");
  fill (0,0,0);
  t = f.get (0, 0, 20, 20);
  map.set (340, 2391, t);
  
  t = f.get (0, 20, 20, 20);
  map.set (325, 2385, t);

  t = f.get (20, 0, 20, 20);
  map.set (369,  1849 , t);    // 3
  
  t = f.get (20, 20, 20, 20);
  map.set (377, 1713, t);      // 4
  
  t = f.get (40, 0, 20, 20);
  map.set (353, 1546, t);      // 5
  
  t = f.get (40, 20, 20, 20);
  map.set (425, 1449, t);      // 6
  
  t = f.get (60, 0, 20, 20);
  map.set (368,  766, t);      // 7
 
  t = f.get (60, 20, 20, 20);
  map.set (321,  777, t);      // 8
  
  t = f.get (80, 0, 20, 20);
  map.set (964,  661, t);      // 9
  
  t = f.get (80, 20, 20, 20);  // 10
  map.set (369,   653, t);
  
  t = f.get (100, 0, 20, 20);
  map.set (2584,  696, t);     // 11
  
  t = f.get (100, 20, 20, 20);
  map.set (1381,  577, t);     // 12
  
  t = f.get (120, 0, 20, 20);
  map.set (2791,  450, t);     // 13
  
  t = f.get (120, 20, 20, 20);
  map.set (2581,  529, t);     // 14
  
  t = f.get (140, 20, 20, 20);
  map.set (2705,  205, t);     // 15
  
  t = f.get (140, 20, 20, 20);
  map.set (2829,  329, t);     // 16
  
  t = f.get (0, 0, 20, 20);
  map.set (1808,  252, t);     // 17
  
  t = f.get (0, 20, 20, 20);
  map.set (2484,  137, t);     // 18
  
  t = f.get (20, 0, 20, 20);
  map.set (555,  179, t);     // 19
   
  t = f.get (20, 20, 20, 20);
  map.set (465,  181, t);     // 20

  t = f.get (40, 0, 20, 20);
  map.set (361,  374, t);     // 21
  
  t = f.get (40, 20, 20, 20);
  map.set (249,  361, t);     // 22

  t = f.get (60, 0, 20, 20);
  map.set (666,  582, t);     // 23
  
  t = f.get (60, 20, 20, 20);
  map.set (365,  497, t);     // 24

  t = f.get (80, 0, 20, 20);
  map.set (2865,  787, t);    // 25
  
  t = f.get (80, 20, 20, 20);
  map.set (2857,  646, t);    //26
  
  t = f.get (100, 0, 20, 20);
  map.set (3030, 1379, t);    // 27
  
  t = f.get (100, 20, 20, 20);
  map.set (3033, 1409, t);    // 28
  
  t = f.get (120, 0, 20, 20);
  map.set (2990, 2624, t);    // 29
  
  t = f.get (120, 20, 20, 20);
  map.set (2990, 2624, t);     // 30
}

void draw ()
{
  image (map, 0, 0);
  text ("1", 340, 2371);
  text ("2",   325, 2375);
  text ("3",   369, 1839);
  text ("4",   377, 1703);
  text ("5",   353, 1536);
  text ("6", 425, 1439);
  text ("7", 368, 756);
  text ("8", 321, 767);
  text ("9",   964,  651);
  text ("10",  369,  643);
  text ("11", 2584,  686);
  text ("12", 1381,  567);
  text ("13", 2791,  440);
  text ("14", 2581,  519);
  text ("15", 2705,  200);
  text ("16", 2829,  319);
  text ("17", 1808,  242);
  text ("18", 2484,  127);
  text ("19",  555,  169);
  text ("20", 465, 160);
  text ("21",  361,  364);
  text ("22", 249,  351);
  text ("23",  666,  572);
  text ("24",  365,  487);
  text ("25", 2865,  777);
  text ("26", 2857,  636);
  text ("27", 3030, 1374);
  text ("28", 3033, 1410);
  text ("End", 2990, 2614);
  text ("End", 2990, 2614);
  save ("z.png");
  noLoop();
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
