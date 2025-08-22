using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cameraFollowAdjust : MonoBehaviour {


	public GameObject hero;
	public float followPoint = 0f;
	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		if (hero.transform.position.y > 0f){
			float tempy = hero.transform.position.y;
			transform.position = new Vector3 (transform.position.x, tempy, transform.position.z);
		}
	}
}
