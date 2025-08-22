using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;

public class playerControllerAvoidance : MonoBehaviour
{
    public float tweenTime = 0.4f;
    public float stepSize = 1;
    public float min_xlimit = -5;
    public float max_xlimit = 5;
    public float min_ylimit = -5;
    public float max_ylimit = 5;
    private float xvalue;
    private float yvalue;
    private float prev_xvalue;
    private float prev_yvalue;
    public Ease myEase;
    //public string mystring = "myEase";
   
    public Animator anim;
    Rigidbody2D mybody;
    private Tween mytween_Horizontal;
    private Tween mytween_Vertical;
    public LayerMask walllayer;

    public bool animation_enable = false;
    public string anim_up;
    public string anim_down;
    public string anim_left;
    public string anim_right;
    private Sequence mySequence;

    // Use this for initialization
    void Start()
    {

        //grab the animator component

        anim = gameObject.GetComponent<Animator>();
        mybody = gameObject.GetComponent<Rigidbody2D>();
        xvalue = (int)transform.position.x;
        yvalue = (int)transform.position.y;
        mySequence = DOTween.Sequence();
        //mytween = mybody.DOMoveX(xvalue, .001f).SetEase(myEase);
        mytween_Vertical = mybody.DOMove(new Vector2(xvalue, yvalue), 0).SetAutoKill(false);
        mytween_Horizontal = mybody.DOMove(new Vector2(xvalue, yvalue), 0).SetAutoKill(false);
    }

    // Update is called once per frame
    void FixedUpdate()
    {
       if (!mytween_Vertical.IsPlaying())
        {
           
            if (Input.GetKeyDown(KeyCode.DownArrow) && !Physics2D.Raycast(transform.position, Vector2.down, 1, walllayer))
            {
                // quantize to the next step if mashing button
                yvalue -= stepSize ;
                // clamp the size
                yvalue = Mathf.Clamp(yvalue, min_ylimit, max_ylimit);
                // the line below is the animation enables the animation
                if (animation_enable) { anim.Play(anim_down, -1, 0); }
                //move the hero
                mytween_Vertical = mybody.DOMove(new Vector2(xvalue, yvalue), tweenTime).SetEase(myEase).SetAutoKill(false);
                //mySequence.Insert(0,mytween_Vertical);


            }
            if (Input.GetKeyDown(KeyCode.UpArrow) && !Physics2D.Raycast(transform.position, Vector2.up, 1, walllayer))
            {

                yvalue += stepSize ;
                yvalue = Mathf.Clamp(yvalue, min_ylimit, max_ylimit);
                if (animation_enable) { anim.Play(anim_up, -1, 0); }

                mytween_Vertical = mybody.DOMove(new Vector2(xvalue, yvalue), tweenTime).SetEase(myEase).SetAutoKill(false);
                //mySequence.Insert(0,mytween_Vertical);

            }
            if (Input.GetKeyDown(KeyCode.LeftArrow) && !Physics2D.Raycast(transform.position, Vector2.left, 1, walllayer))
            {
                xvalue -= stepSize ;
                xvalue = Mathf.Clamp(xvalue, min_xlimit, max_xlimit);
                // the line below is the animation enables the animation
                if (animation_enable) { anim.Play(anim_left, -1, 0); }

                mytween_Vertical = mybody.DOMove(new Vector2(xvalue, yvalue), tweenTime).SetEase(myEase).SetAutoKill(false);
                //mySequence.Insert(0,mytween_Horizontal);
            }

            if (Input.GetKeyDown(KeyCode.RightArrow) && !Physics2D.Raycast(transform.position, Vector2.right, 1, walllayer))
            {
                xvalue += stepSize ;
                xvalue = Mathf.Clamp(xvalue, min_xlimit, max_xlimit);
                if (animation_enable) { anim.Play(anim_right, -1, 0); }
                mytween_Vertical = mybody.DOMove(new Vector2(xvalue, yvalue), tweenTime).SetEase(myEase).SetAutoKill(false);
                // mySequence.Insert(0,mytween_Horizontal);

            }
        }
          
    }

    


      



    }

    

