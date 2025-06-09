from listener import listen_for_triggers

if __name__ == "__main__":
    try:
        listen_for_triggers()
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
