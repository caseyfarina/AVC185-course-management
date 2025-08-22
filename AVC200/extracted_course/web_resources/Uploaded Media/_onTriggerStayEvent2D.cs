using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class _onTriggerStayEvent2D : MonoBehaviour
{

    public int stayFrameDuration = 400;
    int durationCounter = 0;
    public bool destroyObject = true;

    public UnityEvent onTriggerStayEvent;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnTriggerStay2D(Collider2D other)
    {

        durationCounter = durationCounter +1;

        if(durationCounter >= stayFrameDuration)
        {
            onTriggerStayEvent?.Invoke();

            durationCounter = 0;

            if (destroyObject)
            {
                Destroy(other);
            }
            
        }
        
    }
}
