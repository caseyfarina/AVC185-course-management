using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class animationController : MonoBehaviour {

    
    //VARIABLE DECLARATION
    public Animator anim;


    // Use this for initialization
    void Start () {

       anim = gameObject.GetComponent<Animator>();

    }
	
	// Update is called once per frame
	void Update () {

        if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            //play the animation in the animator component MUST BE NAMED CORRECTLY
            anim.Play("forward", -1, 0);
        }

        if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            //play the animation in the animator component MUST BE NAMED CORRECTLY
            anim.Play("backwards", -1, 0);
        }

        if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            //play the animation in the animator component MUST BE NAMED CORRECTLY
            anim.Play("left", -1, 0);
        }

        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            //play the animation in the animator component MUST BE NAMED CORRECTLY
            anim.Play("right", -1, 0);
        }

    }
}
