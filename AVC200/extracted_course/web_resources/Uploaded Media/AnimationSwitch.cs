using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class AnimationSwitch : MonoBehaviour
{


     Animator anim;
    Rigidbody2D mybody;


    
    public float VelocityTHresh = .01f;


    public bool animation_enable = false;
    public string idle;
    public string anim_up;
    public string anim_down;
    public string anim_forward;
    Vector2 velocity;
    Vector2 previousPos;
    public GameObject rigidBodyObject;

    public bool FlipBirdDirection = false;

    // Use this for initialization
    void Start()
    {

        //grab the animator component

        anim = gameObject.GetComponent<Animator>();
        mybody = rigidBodyObject.GetComponent<Rigidbody2D>();

    }
    private void Update()
    {
      // Vector3 fwdDotProduct = Vector3.Dot(transform.forward, velocity);
    }//Vector3 upDotProduct = Vector3.Dot(transform.up, velocity);



    // Update is called once per frame
    void FixedUpdate()
    {
        // velocity = (transform.position - previousPos) / Time.deltaTime;
        // previousPos = transform.position;
        velocity = (mybody.position - previousPos) * 50;
        previousPos = mybody.position;
        Debug.Log(velocity);
        if (Mathf.Abs(velocity.x) > VelocityTHresh || Mathf.Abs(velocity.y) > VelocityTHresh)

        {
            if (Mathf.Abs(velocity.x) > Mathf.Abs(velocity.y))
            {
                if (velocity.x > 0.0f)
                {
                    float birdDirection = 1f;
                    if (FlipBirdDirection)
                    {
                        birdDirection = birdDirection * -1;
                    }
                    
                    
                    transform.localScale = new Vector3(birdDirection, 1f, 1f);
                    

                    if (animation_enable) { anim.Play(anim_forward); }
                }

                if (velocity.x < 0.0f)
                {
                    float birdDirection = -1f;
                    if (FlipBirdDirection)
                    {
                        birdDirection = birdDirection * -1;
                    }

                    transform.localScale = new Vector3(birdDirection, 1f, 1f);

                    if (animation_enable) { anim.Play(anim_forward); }
                }
            }

            if (Mathf.Abs(velocity.y) > Mathf.Abs(velocity.x))
            {
                if (velocity.y > 0.0f)
                {
                    if (animation_enable) { anim.Play(anim_up); }
                }

                if (velocity.y < 0.0f)
                {
                    if (animation_enable) { anim.Play(anim_down); }
                }
            }


        }
        else
        {
            anim.Play(idle);
        }
    }

}



      



    

    

