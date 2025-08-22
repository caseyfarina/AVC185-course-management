using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class _mouseInteraction_OnCollider : MonoBehaviour
{

    public UnityEvent onClicked;
    public UnityEvent onMouseEnter;
    public UnityEvent onMouseOver;
    public UnityEvent onMouseExit;
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
        onClicked?.Invoke();
       // Debug.Log("clicked");
    }

    private void OnMouseEnter()
    {
        onMouseEnter?.Invoke();
        // Debug.Log("clicked");
    }

    private void OnMouseOver()
    {
        onMouseOver?.Invoke();
        // Debug.Log("clicked");
    }

    private void OnMouseExit()
    {
        onMouseExit?.Invoke();
        // Debug.Log("clicked");
    }

}
