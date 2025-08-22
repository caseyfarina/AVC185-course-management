using UnityEngine;
using System.Collections;

public class Rotator_AR : MonoBehaviour {

	//variable declaration for my variable named roataionSpeed
	public float rotationSpeed = .5f;

	
	void Update () 
	{
		
			transform.Rotate (new Vector3 (0, 1, 0) * (Time.deltaTime * rotationSpeed) );
				
		
	}
}	