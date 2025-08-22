using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;



public class collideWinEnd : MonoBehaviour {


	//Declare public canvas object named myText
	public Text myTextwin;
	public Text myTextloose;
	public Animator anim;
	public playerControllerQuantizeTo3 myController;
	// Use this for initialization
	void Start () {


		anim = gameObject.GetComponent<Animator>();
		myController = gameObject.GetComponent<playerControllerQuantizeTo3>();
	}
	
	// Update is called once per frame
	void Update () {

	

	}
	
	void afterDeath (){
		gameObject.SetActive(false);
	}

	// called when the objects collide
	void OnTriggerEnter2D(Collider2D other) {
		
		////////////////////////
		if (other.gameObject.CompareTag("enemy"))
		{
			myTextloose.gameObject.SetActive (true);
			// print a message to the console the hit by enemy
			// Debug.Log ("hit by enemy, press R to restart");

			//turn off the player sprite
			// lowercase "gameObject" refers to the object that the script is on
			myController.enabled = false;
			anim.Play("end",-1,0);
			
		}


		///////////////////

		if (other.gameObject.CompareTag("goal"))
		{	
			// turn on the YOU WIN message when we make contact
			myTextwin.gameObject.SetActive (true);
			myController.enabled = false;
			anim.Play("win",-1,0);


			foreach(GameObject go in GameObject.FindGameObjectsWithTag("enemy")) {
				go.SetActive (false);
			}


		}

	}
}
