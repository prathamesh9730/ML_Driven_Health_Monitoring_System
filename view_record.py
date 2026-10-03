import sheet_handler

if __name__ == "__main__":
    print("📄 Last 5 Records:")
    for row in sheet_handler.get_last_records(5):
        print(row)

    print("\n📄 All Records:")
    for row in sheet_handler.get_all_records():
        print(row)
