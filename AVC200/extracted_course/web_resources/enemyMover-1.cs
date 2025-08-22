using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class enemyMover : MonoBehaviour {
	public float resetPosition = 4f;
	public float stepSize = 1f;
	public float stepTime = 1f;
	Vector3 originalPosition;

	// Use this for initialization
	void Start () {
		originalPosition = gameObject.transform.position;
		InvokeRepeating ("moveThis", stepTime, stepTime);
	}
	
	// Update is called once per frame
	void Update () {
		if (gameObject.transform.position.x > resetPosition) {

			gameObject.transform.localPosition = originalPosition;
		}
		
	}

	void moveThis(){
		gameObject.transform.Translate(Vector3.right*stepSize);
	}
}
