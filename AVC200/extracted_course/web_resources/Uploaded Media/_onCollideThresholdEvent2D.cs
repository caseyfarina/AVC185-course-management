using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class _onCollideThresholdEvent2D : MonoBehaviour
{
    public float threshold = 4.0f;
    public UnityEvent onCollideEvent;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnCollisionEnter2D(Collision2D col)
    {
        if(col.relativeVelocity.magnitude > threshold)
        {
            onCollideEvent?.Invoke();
        }
        
    }
}
