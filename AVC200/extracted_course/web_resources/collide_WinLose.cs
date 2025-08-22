using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;



public class collide_WinLose : MonoBehaviour {


	//Declare public canvas object named myText
	public GameObject myTextwin;
	public GameObject myTextloose;

    public bool animation_enable = false;
    private Animator anim;
    public string endAnimationName;
    public string winAnimationName;
    private playerControllerAvoidanceSound thisPlayerController;



    // Use this for initialization
    void Start () {

        anim = gameObject.GetComponent<Animator>();
        thisPlayerController = gameObject.GetComponent<playerControllerAvoidanceSound>();

    }
	
	// Update is called once per frame
	void Update () {

	

	}

	// called when the objects collide
	void OnTriggerEnter2D(Collider2D other) {
		
		////////////////////////
		if (other.gameObject.CompareTag("enemy"))
		{
			myTextloose.gameObject.SetActive (true);
			// print a message to the console the hit by enemy
			Debug.Log ("hit by enemy, press R to restart");


            // the line below is the animation enables the animation
            if (animation_enable) { anim.Play(endAnimationName, -1, 0); }
            thisPlayerController.enabled = false;
            Collider2D thisCollider = gameObject.GetComponent<Collider2D>();
            thisCollider.enabled = false;

            //turn off the player sprite
            // lowercase "gameObject" refers to the object that the script is on
            //gameObject.SetActive(false);
        }


		///////////////////

		if (other.gameObject.CompareTag("goal"))
		{	
			// turn on the YOU WIN message when we make contact
			myTextwin.gameObject.SetActive (true);

            if (animation_enable) { anim.Play(winAnimationName, -1, 0); }

            foreach (GameObject go in GameObject.FindGameObjectsWithTag("enemy")) {
				go.SetActive (false);
			}


		}

	}
}
