using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ez_on_off_toggle : MonoBehaviour {
    [Header("object one")]
    public string key_one;
    public bool initialState_one = true;
    public GameObject object_one;
    [Space(10)] // 10 pixels of spacing here.
    [Header("object two")]
    public string key_two;
    public bool initialState_two = true;
    public GameObject object_two;
    [Space(10)] // 10 pixels of spacing here.
    [Header("object three")]
    public string key_three;
    public bool initialState_three = true;
    public GameObject object_three;
    [Space(10)] // 10 pixels of spacing here.
    [Header("object four")]
    public string key_four;
    public bool initialState_four = true;
    public GameObject object_four;
    [Space(10)] // 10 pixels of spacing here.
    [Header("object five")]
    public string key_five;
    public bool initialState_five = true;
    public GameObject object_five;
    [Space(10)] // 10 pixels of spacing here.
    [Header("object six")]
    public string key_six;
    public bool initialState_six = true;
    public GameObject object_six;


    // Use this for initialization
    void Start () {
        object_one.SetActive(initialState_one);
        object_two.SetActive(initialState_two);
        object_three.SetActive(initialState_three);
        object_four.SetActive(initialState_four);
        object_five.SetActive(initialState_five);
        object_six.SetActive(initialState_six);
    }
	
	// Update is called once per frame
	void Update () {
        if (Input.GetKeyDown(key_one))
        {
            initialState_one = !initialState_one;
            object_one.SetActive(initialState_one);
        }

        if (Input.GetKeyDown(key_two))
        {
            initialState_two = !initialState_two;
            object_two.SetActive(initialState_two);
        }

        if (Input.GetKeyDown(key_three))
        {
            initialState_three = !initialState_three;
            object_three.SetActive(initialState_three);
        }
        if (Input.GetKeyDown(key_four))
        {
            initialState_four = !initialState_four;
            object_four.SetActive(initialState_four);
        }
        if (Input.GetKeyDown(key_five))
        {
            initialState_five = !initialState_five;
            object_five.SetActive(initialState_five);
        }

        if (Input.GetKeyDown(key_six))
        {
            initialState_six = !initialState_six;
            object_six.SetActive(initialState_six);
        }
    }
}
