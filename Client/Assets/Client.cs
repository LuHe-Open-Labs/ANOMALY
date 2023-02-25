using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Client : MonoBehaviour {

    public Transform star; // Transform de l'étoile
    public float mass; // Masse de la planète
    public float velocity; // Vitesse initiale de la planète
    public float distance; // Distance initiale de la planète à l'étoile
    public float timeScale = 1.0f; // Échelle de temps pour la simulation

    private float G = 6.67430e-11f; // Constante gravitationnelle de Newton
    private Vector3 position;
    private Vector3 velocityVector;

    void Start () {
        // Calcul de la force gravitationnelle initiale entre la planète et l'étoile
        float force = G * star.GetComponent<Rigidbody>().mass * mass / (distance * distance);
        // Calcul de la direction de la force
        Vector3 direction = (star.position - transform.position).normalized;
        // Calcul de la vitesse initiale de la planète
        velocityVector = direction * Mathf.Sqrt(force / mass);
        velocityVector *= velocity / velocityVector.magnitude;
        // Initialisation de la position de la planète
        position = transform.position;
    }

    void FixedUpdate () {
        // Calcul de la distance entre la planète et l'étoile
        float distance = Vector3.Distance(star.position, position);
        // Calcul de la force gravitationnelle entre la planète et l'étoile
        float force = G * star.GetComponent<Rigidbody>().mass * mass / (distance * distance);
        // Calcul de la direction de la force
        Vector3 direction = (star.position - position).normalized;
        // Calcul de l'accélération de la planète
        Vector3 acceleration = direction * (force / mass);
        // Calcul de la nouvelle vitesse de la planète
        velocityVector += acceleration * Time.fixedDeltaTime * timeScale;
        // Calcul de la nouvelle position de la planète
        position += velocityVector * Time.fixedDeltaTime * timeScale;
        // Mise à jour de la position de la planète
        transform.position = position;
    }
}

