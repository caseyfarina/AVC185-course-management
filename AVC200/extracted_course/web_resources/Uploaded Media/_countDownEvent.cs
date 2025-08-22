using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class _countDownEvent : MonoBehaviour
{
    public float startingValue = 10f;
    public float incrementValue = 1f;
    public float thresholdValue = 0f;
    public UnityEvent thresholdSendEvent;
    public UnityEvent<string> sendCurrentValue;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void incrementValueOnce()
    {
        startingValue = startingValue - incrementValue;

        sendCurrentValue.Invoke(startingValue.ToString());
       
        if(startingValue < thresholdValue)
        {

            thresholdSendEvent.Invoke();
        }



    }
}
