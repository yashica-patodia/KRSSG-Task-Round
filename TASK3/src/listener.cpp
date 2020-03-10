#include "ros/ros.h"
#include "turtlesim/Pose.h"
#include <cv_bridge/cv_bridge.h>
#include<opencv2/highgui/highgui.hpp>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <vector>
#include <math.h>
#include<fstream>

using namespace std;
using namespace cv;
#include "std_msgs/MultiArrayLayout.h"
#include "std_msgs/MultiArrayDimension.h"
#include "std_msgs/Float32MultiArray.h"
typedef struct
{
  int x;
  int y;
}coordi;

struct node {

    node *parent;
    coordi position;
    float distance;
};



node start_node;
node end_node;

Mat c_0(1,1,CV_8UC3,Scalar(255,255,255));
Mat c_1(1,1,CV_8UC3,Scalar(0,0,0));
Mat c_3(1,1,CV_8UC3,Scalar(120,120,120));


int villain_Radius=30;

Mat img;
node *T_start[5000],*T_end[5000];
int start_nodes = 0,end_nodes=0;
int reached = 0;
int Line_Radius=20;
vector<coordi>t1,t2;

int present[800][800]={0};



void init(int a,int b,int c,int d)
{
  start_nodes=0;
    end_nodes=0;
    reached=0;
    for(int i=0;i<5000;i++)
    {
      T_start[i]=NULL;
      T_end[i]=NULL;
    }

    while(t1.size())
    {
      t1.pop_back();
    };

    while(t2.size())
    {
      t2.pop_back();

    }

    for(int i=0;i<800;i++)
    {
      for(int j=0;j<800;j++)
      {
        present[i][j]=0;

      }
    }



    start_node.position.x = a;
    start_node.position.y = b;
    start_node.parent = NULL;
    start_node.distance=0;
    present[start_node.position.x][start_node.position.y]=1;



    T_start[start_nodes++] = &start_node;
    end_node.position.x = d;
    end_node.position.y = c;
    end_node.parent=NULL;
    end_node.distance=0;
    present[end_node.position.x][end_node.position.y]=1;
    T_end[end_nodes++]  = &end_node;

    srand(time(NULL));

    Mat element=getStructuringElement(MORPH_RECT,Size(5,5),Point(1,1));
    dilate(img,img,element);

}



int isvalid(int a,int b,Mat c)
{
	if(a>=0&&b>=0&&a<c.rows&& b<c.cols)
		return 1;
	else
		return 0;
}

float node_dist(coordi p, coordi q)
{
  coordi v;
  v.x = p.x - q.x;
  v.y = p.y - q.y;
  return sqrt(pow(v.x, 2) + pow(v.y, 2));
}

int near_node(node rnode, node* Tree[5000],int total_nodes)
{
  float min_dist = 999.0;

  float dist= node_dist(Tree[0]->position, rnode.position);

  int lnode = 0, i = 0;

  coordi target;

  if(Tree==T_start)
  target=end_node.position;
  else
  target=start_node.position;


  for(i=0; i<total_nodes; i++)
  {
    dist = node_dist(Tree[i]->position, rnode.position) +node_dist(Tree[i]->position,target);
    if(dist<min_dist)
    {
      min_dist = dist;
      lnode = i;
    }
  }
  return lnode;
}

coordi stepping(coordi nnode,coordi rnode,int step_size)
{
  coordi interm, step;
  float magn = 0.0, x = 0.0, y = 0.0;
  interm.x = rnode.x - nnode.x;
  interm.y = rnode.y - nnode.y;


  magn = sqrt((interm.x)*(interm.x) + (interm.y)*(interm.y));
  x = (float)(interm.x / magn);
  y = (float)(interm.y / magn);
  step.x = (int)(nnode.x + step_size*x);
  step.y = (int)(nnode.y + step_size*y);
  return step;

}

int check_validity_1(coordi p, coordi q)
{
  coordi large, small;
  int i = 0;
  double slope;
  if(q.x<p.x)
  {
    small = q;
    large = p;
  }
  else
  if(q.x>p.x)
  {
    small = p;
    large = q;
  }
  else
  return -1;

  slope = ((double)large.y - small.y)/((double)large.x - small.x);


  for(i=small.x+1; i<large.x; i++)
  {

    int j = ((i - (small.x))*(slope) + small.y);

    for(int x=-Line_Radius/2;x<Line_Radius/2;x++)
    {
      for(int y=-Line_Radius/2;y<Line_Radius/2;y++)
      {
        if(isvalid(i+y,j+x,img)!=1)
          return 0;

        if(img.at<Vec3b>(i+y,j+x)==c_0.at<Vec3b>(0,0))
          return 0;

      }

    }
  }
  return 1;
}

int check_validity_2(coordi p, coordi q)
{
  coordi large, small;
  int i = 0;
  double slope;
  if(q.y<p.y)
  {
    small = q;
    large = p;
  }
  else
  {
    small = p;
    large = q;
  }

  if(q.y==p.y)
  return -1;

  slope = ((double)large.y - small.y)/((double)large.x - small.x);

  for(i=small.y+1; i<large.y; i++)
  {
    int j = (int)(((i - small.y)/slope) + small.x);

    for(int x=-Line_Radius/2;x<Line_Radius/2;x++)
    {
      for(int y=-Line_Radius/2;y<Line_Radius/2;y++)
      {
        if(isvalid(j+x,i+y,img)!=1)
          return 0;

        if(img.at<Vec3b>(j+x,i+y)==c_0.at<Vec3b>(0,0))
          return 0;

      }

    }
  }
  return 1;
}



void reach(node * a)
{
  node up;
  node f_node= *a;
  up = *(f_node.parent);
  while(1)
  {
    line(img, Point(up.position.y, up.position.x), Point(f_node.position.y, f_node.position.x), Scalar(0, 255, 255), 2, 8);
    if(up.parent == NULL)
      break;
    up = *(up.parent);

    f_node = *(f_node.parent);
  }

}


void data(node* Tree[5000],int total_nodes,node *Check_Tree[5000],int ctotal_nodes,int index)
{ node* a=Tree[total_nodes-1];
  node* b=Check_Tree[index];
  int a_size=0,b_size=0;

  while(b!=NULL)
  {
    t1.push_back(b->position);
    b=b->parent;
    b_size++;
  }

  while(a!=NULL)
  {
    t2.push_back(a->position);
    a=a->parent;
    a_size++;
  }
  int i=a_size-1;
  vector<coordi>Final;
  while(i>=0)
  {
    Final.push_back(t2[i]);
    i--;
  }
  i=0;
  while(i<b_size)
  {
    Final.push_back(t1[i]);
    i++;
  }

  fstream file;

  file.open("/home/parth/catkin_ws/task.txt",ios::out);
  //cout<<"WRITTEN";
  int f_size=(a_size+b_size);

  coordi temp;
  temp.x=-1;
  temp.y=-1;

if(node_dist(Final[0],start_node.position)<node_dist(Final[f_size-1],start_node.position))
  for(int i=0;i<f_size;i++)
  {
    coordi k;

    k.x=(Final[i].y/(float)(img.rows)*11);
    k.y=(11-(Final[i].x/(float)(img.cols)*11));

    if(k.y==temp.y && k.x==temp.x || node_dist(temp,k)<0.5)
      continue;


    temp.y=(11-(Final[i].x/(float)(img.cols)*11));
    temp.x=(Final[i].y/(float)(img.rows)*11);
    if(i==0)
      continue;
    file<<(Final[i].y/(float)(img.cols)*11)<<" "<<(11-(Final[i].x/(float)(img.cols)*11))<<"\n";
  //  cout<<(Final[i].y/(float)(img.rows)*11)<<" "<<(11-(Final[i].x/(float)(img.rows)*11))<<"\n";


  }
else
  for(int i=f_size-1;i>=0;i--)
  { coordi k;
    k.x=(Final[i].y/(float)(img.rows)*11);
    k.y=(11-(Final[i].x/(float)(img.cols)*11));

    if(k.y==temp.y && k.x==temp.x || node_dist(k,temp)<1)
      continue;

    temp.y=(11-(Final[i].x/(float)(img.cols)*11));
    temp.x=(Final[i].y/(float)(img.rows)*11);
    if(i==0)
      continue;

    file<<(Final[i].y/(float)(img.cols)*11)<<" "<<(11-(Final[i].x/(float)(img.cols)*11))<<"\n";
  //  cout<<(Final[i].y/(float)(img.rows)*11)<<" "<<(11-(Final[i].x/(float)(img.rows)*11))<<"\n";

  }

}



node* find(coordi v,node *Tree[5000],int total_nodes)
{
  for(int i=0;i<total_nodes;i++)
  {
    if((Tree[i]->position).x==v.x &&(Tree[i]->position).y==v.y)
    {
      return Tree[i];

    }
  }
  return NULL;
}


int rewire_radius=50;

void rewire(node *Tree[5000],node *stepnode,int total_nodes,node *Check_Tree[5000],int ctotal_nodes)
{

  for(int i=-rewire_radius;i<rewire_radius;i++)
  {
    for(int j=-rewire_radius;j<rewire_radius;j++)
    {
        coordi v;
        v.x=((stepnode->position).x)+i;
        v.y=((stepnode->position).y)+j;



        float d=node_dist(stepnode->position,(stepnode->parent)->position);

        if(isvalid(v.x,v.y,img)==1)
        if((present[v.x][v.y]==1))
        {node *temp=find(v,Tree,total_nodes);
        if(temp==NULL)
        return;
        if(check_validity_1(v,stepnode->position)==1 && check_validity_2(v,stepnode->position)==1 && (node_dist(v,stepnode->position)+(temp->distance))+0.001<(node_dist(stepnode->position,(stepnode->parent)->position)+((stepnode->parent)->distance)))
        {

          //stepnode->parent=find(v,Check_Tree,ctotal_nodes);
          line(img,Point((stepnode->position).y, (stepnode->position).x), Point(((stepnode->parent)->position).y,((stepnode->parent)->position).x), Scalar(0,0,0), 1, 8);
          stepnode->parent=temp;
          stepnode->distance=((stepnode->parent)->distance)+node_dist(v,stepnode->position);

          line(img, Point((stepnode->position).y, (stepnode->position).x), Point(((stepnode->parent)->position).y,((stepnode->parent)->position).x), Scalar(120,120,10),1, 8);

        }
      }
    }
  }

  for(int i=-rewire_radius;i<rewire_radius;i++)
  {
    for(int j=-rewire_radius;j<rewire_radius;j++)
    {
        coordi v;
        v.x=((stepnode->position).x)+i;
        v.y=((stepnode->position).y)+j;

        if(isvalid(v.x,v.y,img)==1)
          if((present[v.x][v.y]==1))
          {
            float d=node_dist(stepnode->position,v);
            node *t=find(v,Tree,total_nodes);

            if(t==NULL)
            return ;
            //t=find(v,Check_Tree,ctotal_nodes);

            if(t->distance>(stepnode->distance+d)&&check_validity_1(v,stepnode->position)==1&&check_validity_2(v,stepnode->position)==1)
            {
              line(img,Point(((t->parent)->position).y, ((t->parent)->position).x),Point(v.y,v.x), Scalar(0,0,0), 1, 8);

              t->parent=stepnode;
              t->distance=stepnode->distance+d;

              line(img,Point(((t->parent)->position).y, ((t->parent)->position).x),Point(v.y,v.x),Scalar(120,120,11),1, 8);
            }


          }

    }

  }
}



int rrt_connect( node* Tree[5000],int *total_nodes,node *Check_Tree[5000],int *ctotal_nodes,int color)
{

  int flag1 = 0, index = 0, flag2 = 0;
  int step_size=5;
  float thresh1=10,thresh2=200;
    node* rnode = new node;
    node* stepnode = new node;
    (rnode->position).x = (rand() % (img.rows));

    (rnode->position).y = (rand() % (img.cols));

  //  cout<<(rnode->position).y<<endl;

    if(isvalid((rnode->position).x,(rnode->position).y,img)==0)
      return -1;

    index = near_node(*rnode,Tree,*total_nodes);

    if((node_dist(rnode->position, Tree[index]->position))<thresh1)
      return -1;

    stepnode->position = stepping(Tree[index]->position, rnode->position,step_size);
    flag1 = check_validity_1(Tree[index]->position, stepnode->position);
    flag2 = check_validity_2(Tree[index]->position, stepnode->position);

    if(flag1!=1||flag2!=1)
      return -1;

    if(1)
    {

      stepnode->position = stepping(Tree[index]->position, rnode->position,step_size);
      present[(stepnode->position).x][(stepnode->position).y]=1;
      Tree[(*total_nodes)++]=stepnode;
      stepnode->parent = Tree[index];

      stepnode->distance =node_dist(Tree[index]->position,stepnode->position)+(stepnode->parent)->distance;

     line(img, Point((stepnode->position).y, (stepnode->position).x), Point(Tree[index]->position.y, Tree[index]->position.x), Scalar(color,255,0), 2, 8);

      int index=near_node(*stepnode,Check_Tree,*ctotal_nodes);

      if((check_validity_1(stepnode->position,Check_Tree[index]->position)) && (check_validity_2(stepnode->position,Check_Tree[index]->position)) && node_dist(stepnode->position,Check_Tree[index]->position)<=step_size)
      {
        reached=1;
          cout<<"DONE"<<endl;
        line(img, Point((stepnode->position).y, (stepnode->position).x), Point(Check_Tree[index]->position.y, Check_Tree[index]->position.x), Scalar(0,255,255), 2, 8);
        reach(stepnode);
        reach(Check_Tree[index]);
        data(Tree,*total_nodes,Check_Tree,*ctotal_nodes,index);
        return 1;

      }

      //rewire(Tree,stepnode,*total_nodes,Check_Tree,*ctotal_nodes);
  //    imshow("window", img);
  //    waitKey(1);
      for(int i=stepnode->position.x - 1; i <= stepnode->position.x + 1; i++)
      {
        for(int j=stepnode->position.y - 1; j <= stepnode->position.y + 1; j++)
        {
          if(isvalid(i,j,img)!=1)
            continue;

          img.at<Vec3b>(i, j)[0] = 110;
          img.at<Vec3b>(i, j)[1] = 255-color;
          img.at<Vec3b>(i, j)[2] = 255;
        }
      }

      return 1;
    }
    return -1;
  }


void render_image(const turtlesim::Pose::ConstPtr& arr)
{ //xcout<<"RENDER";
  for(int i=-1;i<=1;i++)
  {
    for(int j=-1;j<=1;j++)
    {
      img.at<Vec3b>((int)(img.cols-(arr->y)/11.0*img.cols)+i,(int)((arr->x)/11.0*img.rows+j))=c_3.at<Vec3b>(0,0);
    }
  }
  imshow("window",img);
  waitKey(1);

  for(int i=-1;i<=1;i++)
  {
    for(int j=-1;j<=1;j++)
    {
      img.at<Vec3b>((int)(img.cols-(arr->y)/11.0*img.cols)+i,(int)((arr->x)/11.0*img.rows+j))==c_1.at<Vec3b>(0,0);
    }
  }


}





void chatterCallback(const std_msgs::Float32MultiArray::ConstPtr& arr)
{ cout<<"RECEIVED"<<endl;

  img=imread("/home/parth/Downloads/task.png",1);

//  imshow("window",img);
//  waitKey(1);
//  cout<<"RECEIVED"<<endl;
  float a[90];
  int i = 0;

  for(vector<float>::const_iterator it = arr->data.begin(); it != arr->data.end(); ++it)
  {
    a[i]=*it;
    i++;
  //  cout<<"HERE_!"<<endl;
  }


  if(isvalid((int)(img.cols-(a[1])/11.0*img.cols),(int)((a[0])/11.0*img.rows),img)==1)
  {  init(int(img.cols-(a[1])/11.0*img.cols),int((a[0])/11.0*img.rows),550,550);
  //  cout<<"HERE0"<<endl;

  }
  else
  {
//    cout<<"SHIT"<<endl;

  }
  coordi t;
  t.x=(int)(img.cols-(a[3])/11.0*img.cols);
  t.y=(a[2])/11.0*img.rows;

  cout<<node_dist(start_node.position,t)<<endl;
  for(int k=-villain_Radius;k<villain_Radius;k++)
  {
    for(int l=-villain_Radius;l<villain_Radius;l++)
    {
      if(isvalid((int)(img.cols-(a[2])/11.0*img.cols)+l,(int)((a[3])/11.0*img.rows)+k,img)==1)
        img.at<Vec3b>((int)(img.cols-(a[3])/11.0*img.cols)+l,(int)((a[2])/11.0*img.rows)+k)=c_0.at<Vec3b>(0,0);
    }
  }



  for(int i=start_node.position.x - 5; i < start_node.position.x + 5; i++)
  {
    for(int j=start_node.position.y - 5; j < start_node.position.y + 5; j++)
    {
      img.at<Vec3b>(i, j)[0] = 255;
      img.at<Vec3b>(i, j)[1] = 0;
      img.at<Vec3b>(i, j)[2] = 0;
    }
  }

  //imshow("window",img);
  //waitKey(1);


  i=0;
  while(reached==0)
  {   int n=0;
     if((i%2)==0)
      {n= rrt_connect(T_start,&start_nodes,T_end,&end_nodes,255);
      if(n==-1)
        i--;
      }
      else
      {
      n= rrt_connect(T_end,&end_nodes,T_start,&start_nodes,0);
      if(n==-1)
        i--;
      }
      i++;

  }


}

int main(int argc, char **argv)
{

  namedWindow("window",WINDOW_NORMAL);
  img=imread("/home/parth/Downloads/task.png",1);
    for(int i=0;i<img.rows;i++)
        {
          for(int j=0;j<img.cols;j++)
          {
            if(img.at<Vec3b>(i,j)[0]>0&&img.at<Vec3b>(i,j)[0]<255)
                img.at<Vec3b>(i,j)[0]=0;
            if(img.at<Vec3b>(i,j)[1]>0&&img.at<Vec3b>(i,j)[1]<255)
                img.at<Vec3b>(i,j)[1]=0;
            if(img.at<Vec3b>(i,j)[2]>0&&img.at<Vec3b>(i,j)[2]<255)
                img.at<Vec3b>(i,j)[2]=0;

          }
        }

    //imshow("window",img);
    //waitKey(10);
  ros::init(argc, argv, "listener1");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);
  init(50,40,550,500);
  int i=0;
  i=0;
  while(reached==0)
  {   int n=0;
     if((i%2)==0)
      {n= rrt_connect(T_start,&start_nodes,T_end,&end_nodes,255);
      if(n==-1)
        i--;
      }
      else
      {
      n= rrt_connect(T_end,&end_nodes,T_start,&start_nodes,0);
      if(n==-1)
        i--;
      }
      i++;

  }

  ros::Subscriber sub1=n.subscribe("/turtle1/pose",2000,render_image);

  ros::spin();

  return 0;
}
