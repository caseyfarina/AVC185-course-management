using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;



public class collide : MonoBehaviour {


	//Declare public canvas object named myText
	public Text myTextwin;
	public Text myTextloose;
	// Use this for initialization
	void Start () {




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

			//turn off the player sprite
			// lowercase "gameObject" refers to the object that the script is on
			gameObject.SetActive(false);
		}


		///////////////////

		if (other.gameObject.CompareTag("goal"))
		{	
			// turn on the YOU WIN message when we make contact
			myTextwin.gameObject.SetActive (true);



			foreach(GameObject go in GameObject.FindGameObjectsWithTag("enemy")) {
				go.SetActive (false);
			}


		}

	}
}
