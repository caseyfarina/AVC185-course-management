using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class triggerAnimationOff : MonoBehaviour {
	public Animator myAnimator; 
	public string TriggerName = "triggername";
	public string TriggerStopName = "triggerstopname";
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
			// code fpr setting the state in the statemachine
			myAnimator.SetTrigger (TriggerName);
		}

	}

	void OnTriggerExit(Collider Col)
	{
		if (Col.transform.CompareTag ("Player")) 
		{
			// code fpr setting the state in the statemachine
			myAnimator.SetTrigger (TriggerStopName);
			//myAnimator.speed = 0f;
		}

	}


}
