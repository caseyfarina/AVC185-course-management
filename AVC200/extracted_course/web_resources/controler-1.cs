// these are the dictionaries that Unity uses to look up the objects

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class controler : MonoBehaviour {

	public float stepSize = 1f;
	// Use this for initialization
	void Start () {

		//lowercase gameObject refers to this object
		//gameObject.transform.Translate(Vector3.down);
	
	}
	// Update is called once per frame
	void Update () {

		// IF STATEMENT OR CONDITIONAL move right
		if (Input.GetKeyDown(KeyCode.RightArrow))
		{
			//move the game object in the down direction
			gameObject.transform.Translate(Vector3.right*stepSize);
		}

		if (Input.GetKeyDown(KeyCode.LeftArrow))
		{
			//move the game object in the down direction
			gameObject.transform.Translate(Vector3.left*stepSize);
		}

		if (Input.GetKeyDown(KeyCode.UpArrow))
		{
			//move the game object in the down direction
			gameObject.transform.Translate(Vector3.up*stepSize);
		}

		if (Input.GetKeyDown(KeyCode.DownArrow))
		{
			//move the game object in the down direction
			gameObject.transform.Translate(Vector3.down*stepSize);
		}
		

	}
}
