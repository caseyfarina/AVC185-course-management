using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;

public class enemyMover : MonoBehaviour {

	public float tweenTime = 0.4f;
	public int stepSize = 1;

	public float stepRate = 2f;

	public float resetTime = 10f;

	public string animationName;
	private int xvalue;
	private int yvalue;
	private Animator anim;
	Rigidbody2D mybody;
	private Vector3 startPosition;

	// Use this for initialization
	void Start () {
		startPosition = transform.position;
		anim = gameObject.GetComponent<Animator>();
		mybody = gameObject.GetComponent<Rigidbody2D>();
		xvalue = (int)transform.position.x;
		yvalue = (int)transform.position.y;

		InvokeRepeating("mover", stepRate,stepRate);
		InvokeRepeating("resetPosition",resetTime,resetTime);
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	void resetPosition (){
		mybody.position = startPosition;
	}

	void mover () {

		xvalue = stepSize +  ((int)mybody.position.x);
			 //play the animation in the animator component MUST BE NAMED CORRECTLY
			 anim.Play(animationName,-1,0);
			
			 //DOMoveY this is the move function
			 mybody.DOMoveX(xvalue, tweenTime).SetEase(Ease.OutBack);
	}
}
