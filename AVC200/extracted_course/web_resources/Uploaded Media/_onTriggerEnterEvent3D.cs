using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class _onTriggerEnterEvent3D : MonoBehaviour
{

    public UnityEvent onTriggerEnterEvent;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnTriggerEnter(Collider other)
    {
        onTriggerEnterEvent?.Invoke();
    }
}
