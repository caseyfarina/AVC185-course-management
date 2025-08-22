using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class restartAnyScene : MonoBehaviour {
	
	//this is how you make a public variable
	//use a standard ACSII key
	public string restartKey = "r";
	
	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		//if we press "r" reload the game
		if (Input.GetKeyDown (restartKey)) {
		//find out the name of the name of the current scene
		//stor name in variable myscene
			Scene myscene = SceneManager.GetActiveScene();
			//use the scene variable to restart
			SceneManager.LoadScene (myscene.name);
		}
	}
}
