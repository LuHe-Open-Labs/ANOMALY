using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SolarSystem : MonoBehaviour
{
    readonly float G = 0.000295912f;
    public GameObject[] celestials;

    // Start is called before the first frame update
    void Start()
    {
        celestials = GameObject.FindGameObjectsWithTag("Celestial");
        DrawOrbit();
        InitialVelocity();
    }

    // Update is called once per frame
    void Update()
    {

    }

    private void FixedUpdate()
    {
        Gravity();
    }

    void Gravity()
    {
        foreach(GameObject a in celestials)
        {
            foreach(GameObject b in celestials)
            {
                if(!a.Equals(b))
                {
                    float m1 = a.GetComponent<Rigidbody>().mass;
                    float m2 = b.GetComponent<Rigidbody>().mass;
                    float r = Vector3.Distance(a.transform.position, b.transform.position);

                    a.GetComponent<Rigidbody>().AddForce((b.transform.position - a.transform.position).normalized * (G * (m1 * m2) / (r * r)));
                }
            }
        }
    }

    void InitialVelocity()
    {
        foreach(GameObject a in celestials)
        {
            foreach(GameObject b in celestials)
            {
                if (!a.Equals(b))
                {
                    float m2 = b.GetComponent<Rigidbody>().mass;
                    float r = Vector3.Distance(a.transform.position, b.transform.position);
                    a.transform.LookAt(b.transform);

                    a.GetComponent<Rigidbody>().velocity += a.transform.right * Mathf.Sqrt((G * m2) / r);
                }
            }
        }
    }

    void DrawOrbit()
    {
        foreach(GameObject c in celestials)
        {
            if(c.name == "Sun")
            {
                continue;
            }

            LineRenderer lineRenderer = c.AddComponent<LineRenderer>();
            lineRenderer.material = new Material(Shader.Find("Sprites/Default"));
            lineRenderer.startColor = Color.white;
            lineRenderer.endColor = Color.white;
            lineRenderer.startWidth = 10f;
            lineRenderer.endWidth = 10f;
            lineRenderer.positionCount = 360;

            float r = Vector3.Distance(c.transform.position, GameObject.Find("Sun").transform.position);
            float x;
            float y = 0f;
            float z;
            float angle = 20f;

            for (int i = 0; i < 360; i++)
            {
                x = Mathf.Sin(Mathf.Deg2Rad * angle) * r;
                z = Mathf.Cos(Mathf.Deg2Rad * angle) * r;

                lineRenderer.SetPosition(i, new Vector3(x, y, z));

                angle += (360f / 360f);
            }
        }
    }
}