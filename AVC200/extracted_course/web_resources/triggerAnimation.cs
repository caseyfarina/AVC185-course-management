using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class triggerAnimation : MonoBehaviour {
	public Animator myAnimator; 
	public string TriggerName = "triggername";
	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	void OnTriggerEnter(Collider Col)
	{
		if (Col.transform.CompareTag ("Player")) 
		{

			myAnimator.SetTrigger (TriggerName);
		}

	}
}
