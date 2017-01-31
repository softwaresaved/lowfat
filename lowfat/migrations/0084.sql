UPDATE django_content_type SET app_label="lowfat" WHERE app_label="fat";
ALTER TABLE fat_blog RENAME TO lowfat_blog;
ALTER TABLE fat_blogsentmail RENAME TO lowfat_blogsentmail;
ALTER TABLE fat_claimant RENAME TO lowfat_claimant;
ALTER TABLE fat_expense RENAME TO lowfat_expense;
ALTER TABLE fat_expensesentmail RENAME TO lowfat_expensesentmail;
ALTER TABLE fat_fund RENAME TO lowfat_fund;
ALTER TABLE fat_fundsentmail RENAME TO lowfat_fundsentmail;
ALTER TABLE fat_generalsentmail RENAME TO lowfat_generalsentmail;
UPDATE django_migrations SET app='lowfat' WHERE app='fat';
.quit
