import mlflow


def run_demo_experiment() -> None:
    """Simple MLflow demo for the event booking scenario.

    This does not train a real ML model; it just simulates
    logging of metrics such as successful and failed bookings.
    """

    successful_bookings = 80
    failed_bookings = 20
    conversion_rate = successful_bookings / (successful_bookings + failed_bookings)

    mlflow.set_experiment("event_booking_scenario")
    with mlflow.start_run(run_name="booking_conversion_demo"):
        mlflow.log_param("scenario", "event_booking")
        mlflow.log_metric("successful_bookings", successful_bookings)
        mlflow.log_metric("failed_bookings", failed_bookings)
        mlflow.log_metric("conversion_rate", conversion_rate)

        print("Logged metrics to MLflow. Open 'mlflow ui' to inspect.")


if __name__ == "__main__":
    run_demo_experiment()
