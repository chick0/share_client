#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from sys import argv

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from module import models
from module.conf import conf


Dashboard = uic.loadUiType(path.join("ui", "dashboard.ui"))[0]


class MainWindow(QMainWindow, Dashboard):
    def resizeEvent(self, event):
        self.resize(810, 530)

    def refresh_file(self):
        self.idx = None
        self.fileList.clear()

        session = self.session()
        for ctx in session.query(models.File).all():
            self.fileList.addItem(ctx.idx)

    def refresh_report(self):
        self.md5 = None
        self.reportList.clear()

        session = self.session()
        for ctx in session.query(models.Report).all():
            self.reportList.addItem(ctx.md5)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("데이터베이스 관리도구")

        self.engine = create_engine(f"mysql://{conf['account']['user']}:{conf['account']['password']}"
                                    f"@{conf['database']['host']}/{conf['database']['database']}?charset=utf8")
        self.session = sessionmaker(bind=self.engine)

        self.refresh_file()
        self.refresh_report()

        # event
        self.fileList.itemClicked.connect(self.on_file_click)
        self.fileRefresh.clicked.connect(self.refresh_file)
        self.fileReport.clicked.connect(self.file_report)
        self.fileDelete.clicked.connect(self.delete_file)

        self.reportList.itemClicked.connect(self.on_report_click)
        self.reportRefresh.clicked.connect(self.refresh_report)
        self.reportSave.clicked.connect(self.save_report)
        self.reportBan.clicked.connect(self.ban)
        self.reportDelete.clicked.connect(self.delete_report)

        # var
        self.idx = None
        self.md5 = None

    def on_file_click(self, obj):
        idx = obj.text()
        if self.idx != idx:
            self.idx = idx

            session = self.session()
            ctx = session.query(models.File).filter_by(
                idx=idx
            ).first()

            self.fileStatus.clear()
            self.fileStatus.addItem(f"고유번호\t{ctx.idx}")
            self.fileStatus.addItem(f"파일명\t{ctx.filename}")
            self.fileStatus.addItem(f"업로드\t{ctx.upload}")
            self.fileStatus.addItem(f"MD5\t{ctx.md5}")
            self.fileStatus.addItem(f"파일 크기\t{ctx.size/1024/1024:.2f}MB")

    def file_report(self):
        if self.idx is None:
            QMessageBox.critical(self, "오류", "선택된 파일이 없습니다")
            return

        session = self.session()
        ctx = session.query(models.File).filter_by(
            idx=self.idx
        ).first()

        session.add(
            models.Report(
                md5=ctx.md5,
                text=f"idx={ctx.idx}\n{ctx.filename}"
            )
        )

        session.commit()
        self.refresh_report()

    def delete_file(self):
        if self.idx is None:
            QMessageBox.critical(self, "오류", "선택된 파일이 없습니다")
            return

        session = self.session()
        session.query(models.File).filter_by(
            idx=self.idx
        ).delete()
        session.commit()
        self.refresh_file()

    def on_report_click(self, obj):
        if self.md5 is None:
            QMessageBox.critical(self, "오류", "선택된 신고가 없습니다")
            return

        md5 = obj.text()
        if self.md5 != md5:
            self.md5 = md5

            session = self.session()
            ctx = session.query(models.Report).filter_by(
                md5=md5
            ).first()

            self.reportContent.setPlainText(ctx.text)
            self.reportStatus.setText(f"신고 날짜 : {ctx.upload}\t차단 여부 : {ctx.ban}")

    def save_report(self):
        if self.md5 is None:
            QMessageBox.critical(self, "오류", "선택된 신고가 없습니다")
            return

        session = self.session()
        ctx = session.query(models.Report).filter_by(
            md5=self.md5
        ).first()
        ctx.text = self.reportContent.toPlainText()
        session.commit()

        self.refresh_report()

    def ban(self):
        if self.md5 is None:
            QMessageBox.critical(self, "오류", "선택된 신고가 없습니다")
            return

        session = self.session()
        ctx = session.query(models.Report).filter_by(
            md5=self.md5
        ).first()
        ctx.ban = True
        session.commit()

        self.refresh_report()

    def delete_report(self):
        if self.md5 is None:
            QMessageBox.critical(self, "오류", "선택된 신고가 없습니다")
            return

        session = self.session()
        session.query(models.Report).filter_by(
            md5=self.md5
        ).delete()
        session.commit()
        self.refresh_report()


if __name__ == "__main__":
    app = QApplication(argv)

    window = MainWindow()
    window.show()

    app.exec()
