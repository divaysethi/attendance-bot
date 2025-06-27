from datetime import datetime, timedelta  # Add timedelta

@app.route("/slack/<command>", methods=["POST"])
def handle_command(command):
    user_id = request.form.get("user_id")
    user_name = request.form.get("user_name")
    channel_name = request.form.get("channel_name")
    command = command.lower()
    now_str = datetime.now().strftime("%H:%M:%S")

    if channel_name != "time-stuff":
        return jsonify({
            "response_type": "ephemeral",
            "text": "⛔ This command can only be used in the #time-stuff channel."
        })

    if command not in COMMAND_FIELD_MAP:
        return jsonify({"text": "Unknown command."})

    page_id = find_or_create_row(user_id, user_name)

    if command in ["checkin", "breakstart", "breakend"]:
        field = COMMAND_FIELD_MAP[command]
        update_field(page_id, field, now_str)
        return jsonify({"text": f"{command.capitalize()} logged at {now_str}"})

    elif command == "checkout":
        # Log checkout first
        field = COMMAND_FIELD_MAP[command]
        update_field(page_id, field, now_str)

        # Fetch existing fields
        page = notion.pages.retrieve(page_id=page_id)
        props = page["properties"]

        def get_time(prop):
            try:
                return datetime.strptime(
                    props.get(prop, {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "%H:%M:%S"
                )
            except:
                return None

        checkin = get_time("Check-in")
        checkout = datetime.strptime(now_str, "%H:%M:%S")
        break_start = get_time("Break Start")
        break_end = get_time("Break End")

        if checkin:
            total_work = checkout - checkin
            break_duration = (break_end - break_start) if break_start and break_end else timedelta(0)
            total_effective = total_work - break_duration
            total_hours = f"{total_effective.seconds // 3600}h {(total_effective.seconds % 3600) // 60}m"
            update_field(page_id, "Total Hours", total_hours)
        else:
            total_hours = "N/A"

        return jsonify({"text": f"✅ Checkout logged at {now_str}\n🕒 Total Hours: {total_hours}"})

    elif command == "totaltime":
        return jsonify({"text": "Total time today: 7h 45m (placeholder)"})

    elif command == "todayslogs":
        page = notion.pages.retrieve(page_id=page_id)
        props = page["properties"]

        def get_field(name):
            return props.get(name, {}).get("rich_text", [{}])[0].get("text", {}).get("content", "—")

        checkin = get_field("Check-in")
        checkout = get_field("Check-out")
        breakstart = get_field("Break Start")
        breakend = get_field("Break End")
        total = get_field("Total Hours")

        text = (
            f"*Today's Logs for {user_name}*\n"
            f"> 🟢 Check-in: {checkin}\n"
            f"> 🔴 Checkout: {checkout}\n"
            f"> ☕ Break Start: {breakstart}\n"
            f"> 🧍‍♂️ Break End: {breakend}\n"
            f"> ⏱ Total Hours: {total}"
        )
        return jsonify({"response_type": "ephemeral", "text": text})

    return jsonify({"text": "Command handled."})
