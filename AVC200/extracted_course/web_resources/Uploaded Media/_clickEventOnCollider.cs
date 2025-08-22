using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class _clickEventOnCollider : MonoBehaviour
{

    public UnityEvent onClickedEvent;
    // Start is called before the first frame update
    void Start()
    {

        // onClickedEvent = new UnityEvent();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnMouseDown()
    {
        onClickedEvent?.Invoke();
       // Debug.Log("clicked");
    }


}
