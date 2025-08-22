using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class playerTimer : MonoBehaviour
{
    public GameObject timerObject;
    private TextMeshProUGUI timerText;
    public GameObject LoseMessage;
    public ParticleSystem BlazeOfGlory;
    public GameObject attachBot;

    public string pickupTag = "PickUp";
    public float StartTime = 60f;
    public float PickUpTime = 20f;
    private float PickUpTotal = 0f;
    public string countdownPrefix = "Find Energy within  ";
    private float countdown = 0;
    private PlayerControllerCamera thisController;
    //private float originalTime;

    //add time for each pickup X
    //find energy within X
    //gameover for time runningout
    //turn off the bot

    // Start is called before the first frame update
    void Start()
    {   
        timerText = timerObject.GetComponent<TextMeshProUGUI>();
        thisController = GetComponent<PlayerControllerCamera>();
    }

    // Update is called once per frame
    void Update()
    {   
        countdown = Mathf.RoundToInt((StartTime + PickUpTotal)- Time.timeSinceLevelLoad);
        countdown = Mathf.Clamp(countdown, -.3f, 9000f);


        timerText.text = countdownPrefix + countdown.ToString();
        
        if(countdown == 0f)
        {
            dead();
        }
    }

    void OnTriggerEnter(Collider other)
    {
        // ..and if the game object we intersect has the tag 'Pick Up' assigned to it..
        if (other.gameObject.CompareTag(pickupTag))
        {

            PickUpTotal = PickUpTotal + PickUpTime;

        }
    }

    void dead()
    {
           // turn on the lose message
        LoseMessage.SetActive(true);

        timerObject.SetActive(false);

        thisController.enabled = false;

        BlazeOfGlory.Play();

        attachBot.SetActive(false);

        Rigidbody thisbody = GetComponent<Rigidbody>();

        thisbody.AddForce(new Vector3(0, 30f, 0));
        
    }
}
